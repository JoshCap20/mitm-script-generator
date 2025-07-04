from typing import Dict, List
from models import Option

def make(option: Option) -> str:
    # TODO: Implement blockDomainsByList and blockCommonTrackingPatternsByRegex
  # Convert enums to their string values for headers and overrides
    allowed_headers: List[str] = [h.value for h in option.allowedHeaders]
    header_overrides: Dict[str, str] = {h.value: v for h, v in option.headerOverrides.items()}
    return f'''\
import re
from typing import Dict, List
from mitmproxy import http
ALLOWED_HEADERS: List[str] = {allowed_headers}
HEADER_OVERRIDES: Dict[str, str] = {header_overrides}
BLOCKED_DOMAINS: List[str] = {option.blockedDomains}
BLOCKED_PATTERNS: List[re.Pattern[str]] = {option.blockedDomainPatterns}
def request(flow: http.HTTPFlow) -> None:
    header_allowlist: set[str] = set(ALLOWED_HEADERS)
    # Remove not allowlisted headers
    for header in list(flow.request.headers.keys()):
        if header not in header_allowlist:
            del flow.request.headers[header]
    # Set header overrides
    for header, value in HEADER_OVERRIDES.items():
        flow.request.headers[header] = value
    # Check if domain blocked
    if isBlockedDomain(flow.request.pretty_host):
        flow.response = http.Response.make(
            403,
            b"Blocked by mitmproxy: Domain is blocked",
            {{"Content-Type": "text/plain"}}
        )
        return
    # Block by URL pattern
    for pattern in BLOCKED_PATTERNS:
        if pattern.search(flow.request.pretty_url):
            flow.response = http.Response.make(
                403,
                b"Blocked by mitmproxy: URL pattern is blocked",
                {{"Content-Type": "text/plain"}}
            )
            return
def isBlockedDomain(domain: str) -> bool:
    return any(blocked_domain.lower() in domain.lower() for blocked_domain in BLOCKED_DOMAINS)
'''