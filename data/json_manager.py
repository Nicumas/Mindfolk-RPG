import json
import os
import sys

def resource_path(rel_path):
    base = getattr(sys, "_MEIPASS", os.path.abspath("."))
    return os.path.join(base, rel_path)

class jsonManager:
    @staticmethod
    def load_json(file_path: str) -> dict:
        path = resource_path(file_path)
        with open(path, "r", encoding="utf-8") as file:
            return json.load(file)

    @staticmethod
    def save_json(file_path: str, data: dict):
        path = resource_path(file_path)
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, "w", encoding="utf-8") as file:
            json.dump(data, file, ensure_ascii=False, indent=4)

    @staticmethod
    def update_json(file_path: str, key: str, value) -> None:
        data = jsonManager.load_json(file_path)
        data[key] = value
        jsonManager.save_json(file_path, data)

    @staticmethod
    def get_value(file_path: str, key: str):
        data = jsonManager.load_json(file_path)
        return data.get(key, None)