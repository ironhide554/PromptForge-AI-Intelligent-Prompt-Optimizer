import json
import sqlite3
from pathlib import Path
from datetime import datetime

DATA_DIR = Path("data")
DATA_DIR.mkdir(exist_ok=True)
HISTORY_JSON_FILE = DATA_DIR / "history.json"
HISTORY_DB_FILE = DATA_DIR / "history.db"

def _get_connection():
    conn = sqlite3.connect(HISTORY_DB_FILE)
    conn.row_factory = sqlite3.Row
    return conn

def _init_db():
    conn = _get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT,
            original_prompt TEXT,
            optimized_prompt TEXT,
            category TEXT,
            score INTEGER,
            target_model TEXT,
            style TEXT
        )
    """)
    conn.commit()
    conn.close()

def _migrate_json_to_db():
    if HISTORY_JSON_FILE.exists():
        try:
            with open(HISTORY_JSON_FILE, "r", encoding="utf-8") as f:
                history = json.load(f)
            
            conn = _get_connection()
            cursor = conn.cursor()
            
            for item in history:
                cursor.execute("""
                    INSERT INTO history (timestamp, original_prompt, optimized_prompt, category, score, target_model, style)
                    VALUES (?, ?, ?, ?, ?, ?, ?)
                """, (
                    item.get("timestamp", ""),
                    item.get("original_prompt", ""),
                    item.get("optimized_prompt", ""),
                    item.get("category", "General"),
                    item.get("score", 0),
                    item.get("target_model", "ChatGPT"),
                    item.get("style", "Professional")
                ))
            
            conn.commit()
            conn.close()
            
            # Backup json and remove it to prevent re-migration
            backup_file = DATA_DIR / "history.json.bak"
            HISTORY_JSON_FILE.rename(backup_file)
        except Exception as e:
            print(f"Error migrating JSON to SQLite: {e}")

# Initialize and migrate on module load
_init_db()
_migrate_json_to_db()

def load_history():
    try:
        conn = _get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM history ORDER BY id ASC")
        rows = cursor.fetchall()
        conn.close()
        
        # Convert rows back to dict format expected by the app
        history = []
        for row in rows:
            history.append({
                "id": row["id"],
                "timestamp": row["timestamp"],
                "original_prompt": row["original_prompt"],
                "optimized_prompt": row["optimized_prompt"],
                "category": row["category"],
                "score": row["score"],
                "target_model": row["target_model"],
                "style": row["style"]
            })
        return history
    except Exception:
        return []

def save_history(history):
    # This function previously dumped the whole list to JSON.
    # In UI, it's called with save_history([]) to clear history, or when deleting a single item.
    # To support this, we'll clear the table and insert the provided list.
    try:
        conn = _get_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM history")
        
        for item in history:
            cursor.execute("""
                INSERT INTO history (timestamp, original_prompt, optimized_prompt, category, score, target_model, style)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (
                item.get("timestamp", ""),
                item.get("original_prompt", ""),
                item.get("optimized_prompt", ""),
                item.get("category", "General"),
                item.get("score", 0),
                item.get("target_model", "ChatGPT"),
                item.get("style", "Professional")
            ))
        conn.commit()
        conn.close()
    except Exception as e:
        print(f"Error saving history: {e}")

def add_to_history(original, optimized, category, score, target_model, style):
    try:
        conn = _get_connection()
        cursor = conn.cursor()
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        cursor.execute("""
            INSERT INTO history (timestamp, original_prompt, optimized_prompt, category, score, target_model, style)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (timestamp, original, optimized, category, score, target_model, style))
        conn.commit()
        conn.close()
    except Exception as e:
        print(f"Error adding to history: {e}")
