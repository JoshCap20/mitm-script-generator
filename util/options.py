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

lax_option: Option = Option(
    title="Lax",
    description="Headers are unmodified, but blocks known trackers, ads, spam and malware.",
    blockedDomains=COMMON_BLOCKED_DOMAINS,
    blockedDomainPatterns=COMMON_TRACKING_PATTERNS,
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
        CommonHeaders.USER_AGENT.value.upper(),
        CommonHeaders.ACCEPT.value,
        CommonHeaders.ACCEPT_ENCODING.value,
        CommonHeaders.ACCEPT_LANGUAGE.value,
        CommonHeaders.AUTHORIZATION.value,
        CommonHeaders.AUTHORIZATION.value.upper()
    ],
    headerOverrides={
        CommonHeaders.USER_AGENT.value: "Mozilla/5.0 (compatible)",
        CommonHeaders.USER_AGENT.value.upper(): "Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:47.0) Gecko/20100101 Firefox/47.0",
    },
)

secure_option_with_cookies: Option = Option(
    title="Secure with cookies",
    description="Block known trackers, malware and spam. Allows cookies, but no tracking headers.",
    blockedDomains=COMMON_BLOCKED_DOMAINS,
    blockedDomainPatterns=COMMON_TRACKING_PATTERNS,
    allowedHeaders=[
        CommonHeaders.USER_AGENT.value,
        CommonHeaders.USER_AGENT.value.upper(),
        CommonHeaders.ACCEPT.value,
        CommonHeaders.ACCEPT_ENCODING.value,
        CommonHeaders.ACCEPT_LANGUAGE.value,
        CommonHeaders.AUTHORIZATION.value,
        CommonHeaders.AUTHORIZATION.value.upper(),
        CommonHeaders.COOKIE.value
    ],
    headerOverrides={
        CommonHeaders.USER_AGENT.value: "Mozilla/5.0 (compatible)",
        CommonHeaders.USER_AGENT.value.upper(): "Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:47.0) Gecko/20100101 Firefox/47.0",
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
fort_knox_option: Option = Option(
    title="Fort Knox",
    description="Blocks all requests.",
    blockedDomains={OverrideOptions.ALL.value},
    blockedDomainPatterns=[],
    allowedHeaders=[OverrideOptions.NONE.value],
    headerOverrides={},
)

OPTIONS_LIST: list[Option] = [passthrough_option, secure_option, brick_wall_option, secure_option_with_cookies, lax_option, fort_knox_option]

