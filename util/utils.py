from datetime import datetime

from models import Option
from options import OPTIONS_LIST

def get_timestamp() -> str:
    return datetime.now().strftime("%Y%m%d_%H%M%S")

def get_option_by_title(title: str) -> Option:
    for option in OPTIONS_LIST:
        if option.title.lower() == title.lower():
            return option
    raise ValueError(f"Option with title '{title}' not found.")