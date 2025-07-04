
import re
from typing import List, Dict, Set
from dataclasses import dataclass

@dataclass(frozen=True)
class Option:
    title: str
    description: str
    blockedDomains: Set[str]
    blockedDomainPatterns: List[re.Pattern[str]]
    allowedHeaders: List[str]
    headerOverrides: Dict[str, str]
