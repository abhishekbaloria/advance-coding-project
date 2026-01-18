import json
import os
from session import TrainingSession

def get_json_path() -> str:
    base_dir = os.path.dirname(os.path.abspath(__file__))
    data_dir = os.path.join(base_dir, "data")
    os.makedirs(data_dir, exist_ok=True)
    return os.path.join(data_dir, "runs.json")

def save_sessions_to_json(sessions: list[TrainingSession]):
    path = get_json_path()
    payload = [s.to_dict() for s in sessions]
    with open(path, "w", encoding="utf-8") as f:
        json.dump(payload, f, indent=2)

def load_sessions_from_json() -> list[TrainingSession]:
    path = get_json_path()
    if not os.path.exists(path):
        return []
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)
    return [TrainingSession.from_dict(item) for item in data]
