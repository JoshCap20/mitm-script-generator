from models import Option
from template import make as template

def make(option: Option) -> str:
    return template(option)

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

def __generate_filename(option: Option) -> str:
    # Generate a python filename based on time
    from datetime import datetime
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    return f"{option.title.replace(' ', '_').lower()}_{timestamp}.py"

def make_script(option: Option) -> None:
    filename: str = __generate_filename(option)
    print(f"[MAKE_SCRIPT:{option.title}]:: Generating script with filename: {filename}")
    write(make(option), filename)
    print(f"[MAKE_SCRIPT:{option.title}]:: Script generation complete. Saved as {filename}")