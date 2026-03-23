def parse_txt_bytes(file_bytes: bytes) -> str:
    """
    Parse uploaded .txt content into a clean string.
    Tries UTF-8 first, then falls back to latin-1.
    """
    if not file_bytes:
        return ""

    try:
        text = file_bytes.decode("utf-8")
    except UnicodeDecodeError:
        text = file_bytes.decode("latin-1", errors="ignore")

    # Basic cleanup
    text = text.replace("\r\n", "\n").replace("\r", "\n")
    lines = [line.strip() for line in text.split("\n")]
    cleaned = "\n".join(line for line in lines if line)

    return cleaned.strip()