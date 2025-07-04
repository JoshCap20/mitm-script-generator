from models import Option
from constants import CommonHeaders, OverrideOptions
from options import get_option_by_title, options

def make_script_with_option_string(option_string: str) -> str:
    return make(get_option_by_title(option_string))

def make(option: Option) -> str:
    script: str = ""

    return script

def write(content: str, filename: str = "mitm_script.py") -> None:
    print("Removing existing script if it exists")
    import os
    if os.path.exists("mitm_script.py"):
        print(f"Removing existing script {filename}")
        os.remove("mitm_script.py")
        print(f"Existing script removed")
    print("Writing script")
    with open(filename, "w") as f:
        f.write(content)
    print(f"Script written to {filename}")

def make_script(option: Option, filename: str = "mitm_script.py") -> None:
    print(f"Running make_script with option: {option.title} {filename}")
    write(make(option), filename)
    print(f"Script for option '{option.title}' written to {filename}")