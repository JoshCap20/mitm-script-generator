from models import Option
from constants import COMMON_TRACKING_PATTERNS, CommonHeaders,OverrideOptions

passthrough_option: Option = Option(
    title="Passthrough",
    description="No request modifications",
    blockedDomains=[],
    blockedDomainPatterns=[],
    allowedHeaders=[OverrideOptions.ALL],
    headerOverrides={},
)

secure_option: Option = Option(
    title="Secure",
    description="Block know trackers, malware and spam. No cookies, no tracking headers.",
    blockedDomains=[],
    blockedDomainPatterns=COMMON_TRACKING_PATTERNS,
    allowedHeaders=[
        CommonHeaders.USER_AGENT,
        CommonHeaders.ACCEPT,
        CommonHeaders.ACCEPT_ENCODING,
        CommonHeaders.ACCEPT_LANGUAGE,
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
    description="Block domains by list and regex, remove all headers",
    blockedDomains=[],
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