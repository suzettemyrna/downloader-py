# Creates name for downloading file

from urllib.parse import urlparse
import os
import hashlib


def get_filename(link):
    parsed = urlparse(link)
    base = os.path.basename(parsed.path)

    if not base:
        base = "file"

    name, ext = os.path.splitext(base)

    hash_part = hashlib.md5(link.encode()).hexdigest()[:6]

    return f"{name}_{hash_part}{ext}"