from dataclasses import dataclass
from typing import List, Dict, Union
from constants import CommonHeaders, OverrideOptions

@dataclass(frozen=True)
class Option:
    title: str
    description: str
    blockDomainsByList: bool
    blockCommonTrackingPatternsByRegex: bool
    allowedHeaders: List[Union[CommonHeaders, OverrideOptions]]
    headerOverrides: Dict[Union[CommonHeaders, OverrideOptions], str]
