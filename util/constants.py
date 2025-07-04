from enum import Enum
import re


COMMON_TRACKING_PATTERNS: list[re.Pattern[str]] = [
    re.compile(r"([\/?=&]|\.)track(ing)?[\w\-]*[\/?=&]?"),
    re.compile(r"analytics"),
    re.compile(r"pixel"),
    re.compile(r"beacon"),
    re.compile(r"adservice"),
    re.compile(r"doubleclick"),
    re.compile(r"googlesyndication"),
]

class CommonHeaders(Enum):
    USER_AGENT = "User-Agent"
    ACCEPT = "Accept"
    ACCEPT_LANGUAGE = "Accept-Language"
    ACCEPT_ENCODING = "Accept-Encoding"
    CONNECTION = "Connection"
    REFERER = "Referer"
    COOKIE = "Cookie"
    X_FORWARDED_FOR = "X-Forwarded-For"
    X_REAL_IP = "X-Real-IP"
    X_DEVICE_ID = "X-Device-ID"
    X_UIDH = "X-UIDH"
    ETAG = "ETag"
    AUTHORIZATION = "Authorization"
    VIA = "Via"
    FORWARDED = "Forwarded"
    DNT = "DNT"
    SEC_CH_UA = "sec-ch-ua"
    SEC_CH_UA_PLATFORM = "sec-ch-ua-platform"

class OverrideOptions(Enum):
    NONE = "none"
    ALL = "all"