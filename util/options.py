from models import Option
from constants import COMMON_BLOCKED_DOMAINS, COMMON_TRACKING_PATTERNS, CommonHeaders,OverrideOptions

passthrough_option: Option = Option(
    title="Passthrough",
    description="No request modifications",
    blockedDomains=set(),
    blockedDomainPatterns=[],
    allowedHeaders=[OverrideOptions.ALL],
    headerOverrides={},
)

secure_option: Option = Option(
    title="Secure",
    description="Block known trackers, malware and spam. No cookies, no tracking headers.",
    blockedDomains=COMMON_BLOCKED_DOMAINS,
    blockedDomainPatterns=COMMON_TRACKING_PATTERNS,
    allowedHeaders=[
        CommonHeaders.USER_AGENT,
        CommonHeaders.ACCEPT,
        CommonHeaders.ACCEPT_ENCODING,
        CommonHeaders.ACCEPT_LANGUAGE,
        CommonHeaders.AUTHORIZATION
    ],
    headerOverrides={
        CommonHeaders.USER_AGENT: "Mozilla/5.0 (compatible)",
        CommonHeaders.ACCEPT: "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
        CommonHeaders.ACCEPT_ENCODING: "gzip, deflate, br",
        CommonHeaders.ACCEPT_LANGUAGE: "en-US,en;q=0.5",
    },
)

brick_wall_option: Option = Option(
    title="Brick wall",
    description="Block known trackers and malware. Remove all headers.",
    blockedDomains=COMMON_BLOCKED_DOMAINS,
    blockedDomainPatterns=COMMON_TRACKING_PATTERNS,
    allowedHeaders=[OverrideOptions.NONE],
    headerOverrides={},
)

# TODO: Make an allow list domains feature
brick_wall_option: Option = Option(
    title="Fort Knox",
    description="Blocks all requests.",
    blockedDomains=set(OverrideOptions.ALL.value),
    blockedDomainPatterns=[],
    allowedHeaders=[OverrideOptions.NONE],
    headerOverrides={},
)

options = [passthrough_option, secure_option, brick_wall_option]

def get_option_by_title(title: str) -> Option:
    for option in options:
        if option.title.lower() == title.lower():
            return option
    raise ValueError(f"Option with title '{title}' not found.")