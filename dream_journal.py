import json
import os
from datetime import datetime

JOURNAL_FILE = "dreams.json"


def save_dream(dream_data):
    dreams = load_dreams()
    dream_data["date"] = datetime.now().strftime("%Y-%m-%d %H:%M")
    dreams.append(dream_data)
    with open(JOURNAL_FILE, "w", encoding="utf-8") as file:
        json.dump(dreams, file, ensure_ascii=False, indent=2)


def load_dreams():
    if not os.path.exists(JOURNAL_FILE):
        return []
    with open(JOURNAL_FILE, "r", encoding="utf-8") as file:
        return json.load(file)
