from models import Option
from template import make as template
from utils import get_timestamp, get_option_by_title
from options import OPTIONS_LIST
from write import write_file

SCRIPT_FILENAME: str = "mitm_script.py"

def make_script(option: Option) -> None:
    timestamp: str = get_timestamp()
    print(f"[MAKE_SCRIPT:{timestamp}]:: Generating script for option: {option}")
    write_file(template(option, timestamp), timestamp, SCRIPT_FILENAME)
    print(f"[MAKE_SCRIPT:{timestamp}]:: Script generation for option '{option.title}' completed successfully.")

if __name__ == "__main__":
    import sys
    if len(sys.argv) < 2:
        print("Usage: python make.py <option_title>")
        sys.exit(1)
    
    option_title: str = sys.argv[1]
    if option_title not in [opt.title for opt in OPTIONS_LIST]:
        print(f"Error: Option '{option_title}' not found. Available options are: {[opt.title for opt in OPTIONS_LIST]}")
        sys.exit(1)
    make_script(get_option_by_title(option_title))