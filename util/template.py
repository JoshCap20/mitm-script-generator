from typing import Dict, List
from models import Option

def make(option: Option) -> str:
    # TODO: Implement blockDomainsByList and blockCommonTrackingPatternsByRegex
  # Convert enums to their string values for headers and overrides
    allowed_headers: List[str] = [h.value for h in option.allowedHeaders]
    header_overrides: Dict[str, str] = {h.value: v for h, v in option.headerOverrides.items()}
    return f'''\
from mitmproxy import http
from typing import Dict, List

ALLOWED_HEADERS: List[str] = {allowed_headers}
HEADER_OVERRIDES: Dict[str, str] = {header_overrides}

def request(flow: http.HTTPFlow) -> None:
    header_allowlist: set[str] = set(ALLOWED_HEADERS)
    # Remove not allowlisted headers
    for header in list(flow.request.headers.keys()):
        if header not in header_allowlist:
            del flow.request.headers[header]
    # Set header overrides
    for header, value in HEADER_OVERRIDES.items():
        flow.request.headers[header] = value
'''