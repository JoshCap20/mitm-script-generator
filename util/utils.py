from datetime import datetime

def get_timestamp() -> str:
    return datetime.now().strftime("%Y%m%d_%H%M%S")

def capitalize(text: str) -> str:
    if not text:
        return text
    if "-" in text:
        parts = text.split("-")
        return "-".join(part[0].upper() + part[1:] for part in parts)
    if " " in text:
        return " ".join(part[0].upper() + part[1:] for part in text.split(" "))
    return text[0].upper() + text[1:]
