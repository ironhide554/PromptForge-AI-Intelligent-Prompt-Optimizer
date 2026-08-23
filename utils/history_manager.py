import json
from pathlib import Path
from datetime import datetime

DATA_DIR = Path("data")
HISTORY_FILE = DATA_DIR / "history.json"

def load_history():
    if not HISTORY_FILE.exists():
        return []
    try:
        with open(HISTORY_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return []

def save_history(history):
    DATA_DIR.mkdir(exist_ok=True)
    with open(HISTORY_FILE, "w", encoding="utf-8") as f:
        json.dump(history, f, indent=4)

def add_to_history(original, optimized, category, score, target_model, style):
    history = load_history()
    entry = {
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "original_prompt": original,
        "optimized_prompt": optimized,
        "category": category,
        "score": score,
        "target_model": target_model,
        "style": style
    }
    history.append(entry)
    save_history(history)
