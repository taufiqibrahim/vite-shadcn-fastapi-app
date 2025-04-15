import os
import re
import unicodedata


def sanitize_dataset_name(filename, max_length=100):
    # 1. Strip extension
    base_name = os.path.splitext(filename)[0]

    # 2. Normalize unicode (e.g., é -> e)
    base_name = unicodedata.normalize("NFKD", base_name).encode("ascii", "ignore").decode()

    # 3. Replace unsafe characters with space
    base_name = re.sub(r"[^\w\s-]", "", base_name)

    # 4. Collapse multiple spaces/dashes/underscores to single space
    base_name = re.sub(r"[-\s_]+", " ", base_name).strip()

    # 5. Truncate to max length
    if len(base_name) > max_length:
        base_name = base_name[:max_length].rstrip()
    return base_name
