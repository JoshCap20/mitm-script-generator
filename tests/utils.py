import types
from typing import Dict, Any

from src.make import make_script

class MockRequest:
    def __init__(self, headers: Dict[str, str], pretty_host: str, pretty_url: str) -> None:
        self.headers: Dict[str, str] = headers.copy()
        self.pretty_host: str = pretty_host
        self.pretty_url: str = pretty_url

class MockFlow:
    def __init__(self, headers: Dict[str, str], pretty_host: str, pretty_url: str) -> None:
        self.request: MockRequest = MockRequest(headers, pretty_host, pretty_url)
        self.response: Any = None

def get_mock_flow(headers: Dict[str, str], host: str, url: str) -> MockFlow:
    return MockFlow(headers, host, url)

def get_mock_request(headers: Dict[str, str], host: str, url: str) -> MockRequest:
    return MockRequest(headers, host, url)

def _load_script_for_option(option: Any) -> Any:
    make_script(option)
    script = types.ModuleType("script")
    with open("mitm_script.py") as f:
        exec(f.read(), script.__dict__)
    return script