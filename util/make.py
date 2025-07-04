import os
from models import Option
from template import make as template

def make(option: Option) -> str:
    return template(option)

def __remove_file_if_exists(filename: str) -> None:
    if os.path.exists(filename):
        print(f"Removing existing script {filename}")
        os.remove(filename)
        print(f"Existing script removed")
    else:
        print(f"No existing script found at {filename}, nothing to remove")

def __write_file(content: str, filename: str) -> None:
    print(f"Writing script to {filename}")
    with open(filename, "w") as f:
        f.write(content)
        print(f"Script written to {filename}")

def write(content: str, historical_filename: str, main_filename: str = "mitm_script.py") -> None:
    __remove_file_if_exists(historical_filename)
    __remove_file_if_exists(main_filename)
    __write_file(content, historical_filename)
    __write_file(content, main_filename)

def __generate_historical_filename(option: Option) -> str:
    from datetime import datetime
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    return f"{option.title.replace(' ', '_').lower()}_{timestamp}.py"

def make_script(option: Option) -> None:
    historical_filename: str = __generate_historical_filename(option)
    print(f"[MAKE_SCRIPT:{option.title}]:: Generating script with filename: {historical_filename}")
    write(make(option), historical_filename)
    print(f"[MAKE_SCRIPT:{option.title}]:: Script generation complete. Saved as {historical_filename}")

if __name__ == "__main__":
    import sys
    if len(sys.argv) < 2:
        print("Usage: python make.py <option_title>")
        sys.exit(1)
    
    option_title: str = sys.argv[1]
    from options import get_option_by_title, options
    if option_title not in [options.title for options in options]:
        print(f"Error: Option '{option_title}' not found. Available options are: {[opt.title for opt in options]}")
        sys.exit(1)
    try:
        option: Option = get_option_by_title(option_title)
        make_script(option)
    except ValueError as e:
        print(f"Error: {e}")
        sys.exit(1)