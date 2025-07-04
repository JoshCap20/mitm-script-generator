from dataclasses import dataclass
from typing import List, Dict, Union
from constants import CommonHeaders, OverrideOptions

@dataclass(frozen=True)
class Option:
    title: str
    description: str
    blockedDomains: List[str]
    blockedDomainPatterns: List[str]
    allowedHeaders: List[Union[CommonHeaders, OverrideOptions]]
    headerOverrides: Dict[Union[CommonHeaders, OverrideOptions], str]
