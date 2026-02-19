import json
import os
from datetime import date, datetime

def load_logs(file_path: str) -> list:
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            data = json.load(f)
            return data if isinstance(data, list) else []
    except FileNotFoundError:
        return []
    except json.JSONDecodeError:
        return []

def save_logs(file_path: str, logs: list) -> None:
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(logs, f, indent=2)

def already_logged_today(logs: list, schedule_id: int, username: str) -> bool:
    today = date.today().isoformat()
    for item in logs:
        if (
            item.get("schedule_id") == schedule_id
            and item.get("day") == today
            and item.get("username", "").lower() == username.lower()
        ):
            return True
    return False

def add_log(logs: list, schedule_id: int, med_name: str, username: str, status: str) -> list:
    entry = {
        "when": datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S"),
        "day": date.today().isoformat(),
        "schedule_id": schedule_id,
        "med_name": med_name,
        "username": username,
        "status": status,
    }
    logs.insert(0, entry)
    return logs
