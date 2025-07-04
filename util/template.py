from models import Option

def make(option: Option) -> str:
    # TODO: Implement blockDomainsByList and blockCommonTrackingPatternsByRegex
    script = f'''\
from mitmproxy import http
from typing import Dict, List

ALLOWED_HEADERS: List[str] = {option.allowedHeaders}
HEADER_OVERRIDES: Dict[str, str] = {option.headerOverrides}

def request(flow: http.HTTPFlow) -> None:
    allowed_headers: set[str] = set(ALLOWED_HEADERS)
    available_headers: list[str] = list(flow.request.headers.keys()) # type: ignore
    for header in available_headers:
        if header not in allowed_headers:
            del flow.request.headers[header]
    for header, value in HEADER_OVERRIDES.items():
        flow.request.headers[header] = value
'''
    return script