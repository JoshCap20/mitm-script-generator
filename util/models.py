from dataclasses import dataclass
import re
from typing import List, Dict, Union
from constants import CommonHeaders, OverrideOptions

@dataclass(frozen=True)
class Option:
    title: str
    description: str
    blockedDomains: List[str]
    blockedDomainPatterns: List[re.Pattern[str]]
    allowedHeaders: List[Union[CommonHeaders, OverrideOptions]]
    headerOverrides: Dict[Union[CommonHeaders, OverrideOptions], str]
