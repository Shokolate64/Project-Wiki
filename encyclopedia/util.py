import os
from django.conf import settings

ENTRIES_DIR = os.path.join(settings.BASE_DIR, "encyclopedia", "entries")

def list_entries():
    _, _, filenames = next(os.walk(ENTRIES_DIR))
    return list(sorted(filename.replace(".md", "")for filename in filenames))

def save_entry(title, content):
    filepath = os.path.join(ENTRIES_DIR, f"{title}.md")
    with open(filepath, "w") as f:
        f.write(content)

def get_entry(title):
    try:
        with open(os.path.join(ENTRIES_DIR, f"{title}.md")) as f:
            return f.read()
    except FileNotFoundError:
        return None    