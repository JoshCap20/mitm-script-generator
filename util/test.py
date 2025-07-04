import types
import pytest
from typing import Dict, Any, Callable, TypeVar, Generic
from options import OPTIONS_LIST
from make import make_script

T = TypeVar('T')

class MockRequest:
    def __init__(self, headers: Dict[str, str], pretty_host: str, pretty_url: str) -> None:
        self.headers: Dict[str, str] = headers.copy()
        self.pretty_host: str = pretty_host
        self.pretty_url: str = pretty_url

class MockFlow:
    def __init__(self, headers: Dict[str, str], pretty_host: str, pretty_url: str) -> None:
        self.request: MockRequest = MockRequest(headers, pretty_host, pretty_url)
        self.response: Any = None

# --- Assertion helpers (Hamcrest/AssertJ style) ---
class assertThat(Generic[T]):
    def __init__(self, actual: T) -> None:
        self.actual: T = actual
    def is_(self, matcher: Callable[[T], bool]) -> 'assertThat[T]':
        assert matcher(self.actual), f"Assertion failed: {self.actual} does not satisfy matcher {matcher}"
        return self
    def contains(self, item: Any) -> 'assertThat[T]':
        assert item in self.actual, f"Assertion failed: {item} not in {self.actual}"
        return self
    def doesNotContain(self, item: Any) -> 'assertThat[T]':
        assert item not in self.actual, f"Assertion failed: {item} unexpectedly in {self.actual}"
        return self
    def equals(self, expected: Any) -> 'assertThat[T]':
        assert self.actual == expected, f"Assertion failed: {self.actual} != {expected}"
        return self
    def isEmpty(self) -> 'assertThat[T]':
        assert not self.actual, f"Assertion failed: {self.actual} is not empty"
        return self
    def isNotEmpty(self) -> 'assertThat[T]':
        assert self.actual, f"Assertion failed: {self.actual} is empty"
        return self

def allOf(*matchers: Callable[[Any], bool]) -> Callable[[Any], bool]:
    def combined(actual: Any) -> bool:
        return all(m(actual) for m in matchers)
    return combined

def hasKeys(*keys: str) -> Callable[[Dict[str, Any]], bool]:
    def matcher(d: Dict[str, Any]) -> bool:
        return all(k in d for k in keys)
    return matcher

def not_(matcher: Callable[[Any], bool]) -> Callable[[Any], bool]:
    def negated(actual: Any) -> bool:
        return not matcher(actual)
    return negated

# --- Dedicated tests for each option ---
def _load_script_for_option(option: Any) -> Any:
    make_script(option)
    script = types.ModuleType("script")
    with open("mitm_script.py") as f:
        exec(f.read(), script.__dict__)
    return script

def test_passthrough_option() -> None:
    option = next(o for o in OPTIONS_LIST if o.title == "Passthrough")
    script = _load_script_for_option(option)
    # All headers allowed, nothing blocked
    headers = {"user-agent": "ua", "cookie": "c", "x-custom": "v"}
    flow = MockFlow(headers, "notblocked.com", "http://notblocked.com/page")
    script.request(flow)
    assertThat(flow.request.headers).contains("user-agent").contains("cookie").contains("x-custom")
    assertThat(flow.response).is_(lambda r: r is None)
    # Should not block tracker domain
    flow = MockFlow(headers, "tracker.com", "http://tracker.com/page")
    script.request(flow)
    assertThat(flow.response).is_(lambda r: r is None)
    # Should not block tracking pattern
    flow = MockFlow(headers, "notblocked.com", "http://notblocked.com/trackingscript.js")
    script.request(flow)
    assertThat(flow.response).is_(lambda r: r is None)

def test_lax_option() -> None:
    option = next(o for o in OPTIONS_LIST if o.title == "Lax")
    script = _load_script_for_option(option)
    # All headers allowed, but blocks trackers
    headers = {"user-agent": "ua", "cookie": "c", "x-custom": "v"}
    flow = MockFlow(headers, "tracker.com", "http://tracker.com/page")
    script.request(flow)
    assertThat(flow.response).is_(lambda r: r is not None and r.status_code == 403)
    flow = MockFlow(headers, "notblocked.com", "http://notblocked.com/trackingscript.js")
    script.request(flow)
    assertThat(flow.response).is_(lambda r: r is not None and r.status_code == 403)
    flow = MockFlow(headers, "notblocked.com", "http://notblocked.com/page")
    script.request(flow)
    assertThat(flow.response).is_(lambda r: r is None)
    # Headers untouched
    assertThat(flow.request.headers).contains("user-agent").contains("cookie").contains("x-custom")

def test_secure_option() -> None:
    option = next(o for o in OPTIONS_LIST if o.title == "Secure")
    script = _load_script_for_option(option)
    # Only allowed headers, others removed
    headers = {"user-agent": "ua", "USER-AGENT": "UA2", "cookie": "c", "x-custom": "v"}
    flow = MockFlow(headers, "notblocked.com", "http://notblocked.com/page")
    script.request(flow)
    assertThat(flow.request.headers).doesNotContain("x-custom").doesNotContain("cookie")
    assertThat(flow.request.headers).contains("user-agent").contains("USER-AGENT")
    # Header override (case-insensitive)
    if "user-agent" in option.headerOverrides:
        assertThat(flow.request.headers["user-agent"]).equals(option.headerOverrides["user-agent"])
    if "USER-AGENT" in option.headerOverrides:
        assertThat(flow.request.headers["USER-AGENT"]).equals(option.headerOverrides["USER-AGENT"])
    # Block tracker domain
    flow = MockFlow({"user-agent": "ua"}, "tracker.com", "http://tracker.com/page")
    script.request(flow)
    assertThat(flow.response).is_(lambda r: r is not None and r.status_code == 403)
    # Block tracking pattern
    flow = MockFlow({"user-agent": "ua"}, "notblocked.com", "http://notblocked.com/trackingscript.js")
    script.request(flow)
    assertThat(flow.response).is_(lambda r: r is not None and r.status_code == 403)
    # Not blocked
    flow = MockFlow({"user-agent": "ua"}, "notblocked.com", "http://notblocked.com/page")
    script.request(flow)
    assertThat(flow.response).is_(lambda r: r is None)

def test_secure_with_cookies_option() -> None:
    option = next(o for o in OPTIONS_LIST if o.title == "Secure with cookies")
    script = _load_script_for_option(option)
    # Allowed headers, cookies allowed
    headers = {"user-agent": "ua", "cookie": "c", "vscode-machineid": "id", "vscode-sessionid": "sid", "x-custom": "v"}
    flow = MockFlow(headers, "notblocked.com", "http://notblocked.com/page")
    script.request(flow)
    assertThat(flow.request.headers).doesNotContain("x-custom")
    assertThat(flow.request.headers).contains("cookie").contains("vscode-machineid").contains("vscode-sessionid")
    # Block tracker domain
    flow = MockFlow({"user-agent": "ua"}, "tracker.com", "http://tracker.com/page")
    script.request(flow)
    assertThat(flow.response).is_(lambda r: r is not None and r.status_code == 403)
    # Block tracking pattern
    flow = MockFlow({"user-agent": "ua"}, "notblocked.com", "http://notblocked.com/trackingscript.js")
    script.request(flow)
    assertThat(flow.response).is_(lambda r: r is not None and r.status_code == 403)
    # Not blocked
    flow = MockFlow({"user-agent": "ua"}, "notblocked.com", "http://notblocked.com/page")
    script.request(flow)
    assertThat(flow.response).is_(lambda r: r is None)

def test_brick_wall_option() -> None:
    option = next(o for o in OPTIONS_LIST if o.title == "Brick wall")
    script = _load_script_for_option(option)
    # All headers removed
    headers = {"user-agent": "ua", "cookie": "c", "x-custom": "v"}
    flow = MockFlow(headers, "notblocked.com", "http://notblocked.com/page")
    script.request(flow)
    assertThat(flow.request.headers).isEmpty()
    # Block tracker domain
    flow = MockFlow({"user-agent": "ua"}, "tracker.com", "http://tracker.com/page")
    script.request(flow)
    assertThat(flow.response).is_(lambda r: r is not None and r.status_code == 403)
    # Block tracking pattern
    flow = MockFlow({"user-agent": "ua"}, "notblocked.com", "http://notblocked.com/trackingscript.js")
    script.request(flow)
    assertThat(flow.response).is_(lambda r: r is not None and r.status_code == 403)
    # Not blocked
    flow = MockFlow({"user-agent": "ua"}, "notblocked.com", "http://notblocked.com/page")
    script.request(flow)
    assertThat(flow.response).is_(lambda r: r is None)

def test_fort_knox_option() -> None:
    option = next(o for o in OPTIONS_LIST if o.title == "Fort Knox")
    script = _load_script_for_option(option)
    # All requests blocked, all headers removed
    headers = {"user-agent": "ua", "cookie": "c", "x-custom": "v"}
    flow = MockFlow(headers, "notblocked.com", "http://notblocked.com/page")
    script.request(flow)
    assertThat(flow.response).is_(lambda r: r is not None and r.status_code == 403)
    assertThat(flow.request.headers).isEmpty()
    # Block tracker domain
    flow = MockFlow({"user-agent": "ua"}, "tracker.com", "http://tracker.com/page")
    script.request(flow)
    assertThat(flow.response).is_(lambda r: r is not None and r.status_code == 403)
    # Block tracking pattern
    flow = MockFlow({"user-agent": "ua"}, "notblocked.com", "http://notblocked.com/trackingscript.js")
    script.request(flow)
    assertThat(flow.response).is_(lambda r: r is not None and r.status_code == 403)