from datetime import datetime

from models import Option
from options import OPTIONS_LIST

def get_timestamp() -> str:
    return datetime.now().strftime("%Y%m%d_%H%M%S")

def load_domain_file(file_path: str = "blocked_domains.txt") -> set[str]:
    try:
        with open(file_path, "r") as f:
            return set(line.strip().lower() for line in f if line.strip() and not line.startswith("#"))
    except FileNotFoundError:
        print(f"Warning: Blocked domains file '{file_path}' not found. Using empty set.")
        return set()
    except Exception as e:
        raise Exception(f"Error loading blocked domains from '{file_path}': {e}")

def get_option_by_title(title: str) -> Option:
    for option in OPTIONS_LIST:
        if option.title.lower() == title.lower():
            return option
    raise ValueError(f"Option with title '{title}' not found.")