import re
from enum import Enum
from typing import Set

def __load_domain_file(file_path: str = "util/blocked_domains.txt") -> set[str]:
    try:
        with open(file_path, "r") as f:
            return set(line.strip().lower() for line in f if line.strip() and not line.startswith("#"))
    except FileNotFoundError:
        raise FileNotFoundError(f"Blocked domains file '{file_path}' not found. Please ensure it exists.")
    except Exception as e:
        raise Exception(f"Error loading blocked domains from '{file_path}': {e}")

COMMON_BLOCKED_DOMAINS: Set[str] = __load_domain_file()

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
    USER_AGENT = "user-agent"
    ACCEPT = "accept"
    ACCEPT_LANGUAGE = "accept-language"
    ACCEPT_ENCODING = "accept-encoding"
    CONNECTION = "connection"
    REFERER = "referer"
    COOKIE = "cookie"
    X_FORWARDED_FOR = "X-Forwarded-For"
    X_REAL_IP = "X-Real-IP"
    X_DEVICE_ID = "X-Device-ID"
    X_UIDH = "X-UIDH"
    ETAG = "ETag"
    AUTHORIZATION = "authorization"
    VIA = "Via"
    FORWARDED = "Forwarded"
    DNT = "dnt"
    SEC_CH_UA = "sec-ch-ua"
    SEC_CH_UA_PLATFORM = "sec-ch-ua-platform"

class OverrideOptions(Enum):
    NONE = "none"
    ALL = "all"