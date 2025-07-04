from models import Option
from constants import COMMON_BLOCKED_DOMAINS, COMMON_TRACKING_PATTERNS, CommonHeaders,OverrideOptions

passthrough_option: Option = Option(
    title="Passthrough",
    description="No request modifications",
    blockedDomains=set(),
    blockedDomainPatterns=[],
    allowedHeaders=[OverrideOptions.ALL.value],
    headerOverrides={},
)

secure_option: Option = Option(
    title="Secure",
    description="Block known trackers, malware and spam. No cookies, no tracking headers.",
    blockedDomains=COMMON_BLOCKED_DOMAINS,
    blockedDomainPatterns=COMMON_TRACKING_PATTERNS,
    allowedHeaders=[
        CommonHeaders.USER_AGENT.value,
        CommonHeaders.ACCEPT.value,
        CommonHeaders.ACCEPT_ENCODING.value,
        CommonHeaders.ACCEPT_LANGUAGE.value,
        CommonHeaders.AUTHORIZATION.value
    ],
    headerOverrides={
        CommonHeaders.USER_AGENT.value: "Mozilla/5.0 (compatible)",
        CommonHeaders.ACCEPT.value: "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
        CommonHeaders.ACCEPT_ENCODING.value: "gzip, deflate, br",
        CommonHeaders.ACCEPT_LANGUAGE.value: "en-US,en;q=0.5",
    },
)

secure_option_with_cookies: Option = Option(
    title="Secure with cookies",
    description="Block known trackers, malware and spam. Allows cookies, but no tracking headers.",
    blockedDomains=COMMON_BLOCKED_DOMAINS,
    blockedDomainPatterns=COMMON_TRACKING_PATTERNS,
    allowedHeaders=[
        CommonHeaders.USER_AGENT.value,
        CommonHeaders.ACCEPT.value,
        CommonHeaders.ACCEPT_ENCODING.value,
        CommonHeaders.ACCEPT_LANGUAGE.value,
        CommonHeaders.AUTHORIZATION.value,
        CommonHeaders.COOKIE.value
    ],
    headerOverrides={
        CommonHeaders.USER_AGENT.value: "Mozilla/5.0 (compatible)",
        CommonHeaders.ACCEPT.value: "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
        CommonHeaders.ACCEPT_ENCODING.value: "gzip, deflate, br",
        CommonHeaders.ACCEPT_LANGUAGE.value: "en-US,en;q=0.5",
    },
)

brick_wall_option: Option = Option(
    title="Brick wall",
    description="Block known trackers and malware. Remove all headers.",
    blockedDomains=COMMON_BLOCKED_DOMAINS,
    blockedDomainPatterns=COMMON_TRACKING_PATTERNS,
    allowedHeaders=[OverrideOptions.NONE.value],
    headerOverrides={},
)

# TODO: Make an allow list domains feature
brick_wall_option: Option = Option(
    title="Fort Knox",
    description="Blocks all requests.",
    blockedDomains=set(OverrideOptions.ALL.value),
    blockedDomainPatterns=[],
    allowedHeaders=[OverrideOptions.NONE.value],
    headerOverrides={},
)

OPTIONS_LIST: list[Option] = [passthrough_option, secure_option, brick_wall_option, secure_option_with_cookies]

