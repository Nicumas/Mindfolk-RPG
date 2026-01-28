import json

class jsonManager:
    @staticmethod
    def load_json(file_path: str) -> dict:
        with open(file_path, 'r', encoding='utf-8') as file:
            return json.load(file)
        
    def save_json(file_path: str, data: dict):
        with open(file_path, 'w', encoding='utf-8') as file:
            json.dump(data, file, ensure_ascii=False, indent=4)

    def update_json(file_path: str, key: str, value) -> None:
        data = jsonManager.load_json(file_path)
        data[key] = value
        jsonManager.save_json(file_path, data)

    def get_value(file_path: str, key: str):
        data = jsonManager.load_json(file_path)
        return data.get(key, None)