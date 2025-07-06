"""
Migrating currently
"""
import types
from typing import Dict, Any, Callable, TypeVar, Generic

from src.options import OPTIONS_LIST
from src.make import make_script

from tests.utils import MockFlow, MockRequest, load_script_for_option
from tests.data_helper import TestTrackingDomainData

TEST_NOT_TRACKING_DOMAIN_HOST: str = "google.com"
TEST_NOT_TRACKING_DOMAIN_URL: str = "https://google.com"
TEST_COMMON_TRACKING_DOMAIN_HOST: str = "tracking.orixa-media.com"
TEST_COMMON_TRACKING_DOMAIN_URL: str = "https://tracking.orixa-media.com"
TEST_COMMON_TRACKING_PATTERN_HOST = "test.adservice.com"
TEST_COMMON_TRACKING_PATTERN_URL: str = "https://test.adservice.com"

T = TypeVar('T')

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

def test_brick_wall_option() -> None:
    option = next(o for o in OPTIONS_LIST if o.title == "Brick wall")
    script = load_script_for_option(option)
    # All headers removed
    headers = {"user-agent": "ua", "cookie": "c", "x-custom": "v"}
    flow = MockFlow(headers, TEST_NOT_TRACKING_DOMAIN_HOST, TEST_NOT_TRACKING_DOMAIN_URL)
    script.request(flow)
    assertThat(flow.request.headers).isEmpty()
    # Block tracker domain
    flow = MockFlow({"user-agent": "ua"}, TEST_COMMON_TRACKING_DOMAIN_HOST, TEST_COMMON_TRACKING_DOMAIN_URL)
    script.request(flow)
    assertThat(flow.response).is_(lambda r: r is not None and r.status_code == 403)
    # Block tracking pattern
    flow = MockFlow({"user-agent": "ua"}, TEST_COMMON_TRACKING_PATTERN_HOST, TEST_COMMON_TRACKING_PATTERN_URL)
    script.request(flow)
    assertThat(flow.response).is_(lambda r: r is not None and r.status_code == 403)
    # Not blocked
    flow = MockFlow({"user-agent": "ua"}, TEST_NOT_TRACKING_DOMAIN_HOST, TEST_NOT_TRACKING_DOMAIN_URL)
    script.request(flow)
    assertThat(flow.response).is_(lambda r: r is None)

def test_fort_knox_option() -> None:
    option = next(o for o in OPTIONS_LIST if o.title == "Fort Knox")
    script = load_script_for_option(option)
    # All requests blocked, all headers removed
    headers = {"user-agent": "ua", "cookie": "c", "x-custom": "v"}
    flow = MockFlow(headers, TEST_NOT_TRACKING_DOMAIN_HOST, TEST_NOT_TRACKING_DOMAIN_URL)
    script.request(flow)
    assertThat(flow.response).is_(lambda r: r is not None and r.status_code == 403)
    assertThat(flow.request.headers).isEmpty()
    # Block tracker domain
    flow = MockFlow({"user-agent": "ua"}, TEST_COMMON_TRACKING_DOMAIN_HOST, TEST_COMMON_TRACKING_DOMAIN_URL)
    script.request(flow)
    assertThat(flow.response).is_(lambda r: r is not None and r.status_code == 403)
    # Block tracking pattern
    flow = MockFlow({"user-agent": "ua"}, TEST_COMMON_TRACKING_PATTERN_HOST, TEST_COMMON_TRACKING_PATTERN_URL)
    script.request(flow)
    assertThat(flow.response).is_(lambda r: r is not None and r.status_code == 403)