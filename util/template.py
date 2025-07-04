from models import Option

def make(option: Option) -> str:
    # TODO: Implement blockDomainsByList and blockCommonTrackingPatternsByRegex
    return f'''\
from mitmproxy import http
from typing import Dict, List

ALLOWED_HEADERS: List[str] = {option.allowedHeaders}
HEADER_OVERRIDES: Dict[str, str] = {option.headerOverrides}

def request(flow: http.HTTPFlow) -> None:
    header_allowlist: set[str] = set(ALLOWED_HEADERS)
    # Remove not allowlisted headers
    for header in flow.request.headers:
        if header not in header_allowlist:
            del flow.request.headers[header]
    # Set header overrides
    for header, value in HEADER_OVERRIDES.items():
        flow.request.headers[header] = value
'''