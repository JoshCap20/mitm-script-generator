
import os

HISTORY_DIR = "history"
HISTORY_FILENAME_PREFIX = "mitm_script_"
HISTORY_FILENAME_SUFFIX = ".py"

def write_file(content: str, timestamp: str, main_filename: str) -> None:
    if not os.path.exists(HISTORY_DIR):
        os.makedirs(HISTORY_DIR)
    historical_filename = f"{HISTORY_DIR}/{HISTORY_FILENAME_PREFIX}{timestamp}{HISTORY_FILENAME_SUFFIX}"
    def __remove_file_if_exists(filename: str) -> None:
        if os.path.exists(filename):
            print(f"Removing existing script {filename}")
            os.remove(filename)
            print(f"Existing script removed")
    def __write_file(content: str, filename: str) -> None:
        print(f"Writing script to {filename}")
        with open(filename, "w") as f:
            f.write(content)
            print(f"Script written to {filename}")
    __remove_file_if_exists(historical_filename)
    __remove_file_if_exists(main_filename)
    __write_file(content, historical_filename)
    __write_file(content, main_filename)