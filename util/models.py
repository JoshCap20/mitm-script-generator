
import re
from typing import List, Dict, Union, Set
from dataclasses import dataclass
from constants import CommonHeaders, OverrideOptions

@dataclass(frozen=True)
class Option:
    title: str
    description: str
    blockedDomains: Set[str]
    blockedDomainPatterns: List[re.Pattern[str]]
    allowedHeaders: List[Union[CommonHeaders, OverrideOptions]]
    headerOverrides: Dict[Union[CommonHeaders, OverrideOptions], str]
