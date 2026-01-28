import openai
from data.json_manager import jsonManager
import json

YANDEX_CLOUD_FOLDER = jsonManager.get_value("data/data.json", "api_yandex")["YANDEX_CLOUD_FOLDER"]
YANDEX_CLOUD_API_KEY = jsonManager.get_value("data/data.json", "api_yandex")["YANDEX_CLOUD_API_KEY"]

class DeepSeekClient:
    def __init__(self, client=None):
        self.client = openai.OpenAI(
            api_key=YANDEX_CLOUD_API_KEY,
            base_url="https://rest-assistant.api.cloud.yandex.net/v1",
            project=YANDEX_CLOUD_FOLDER
        )

    def send_state(self, state: dict) -> dict:
        try:
            response = self.client.responses.create(
                prompt={
                    "id": "fvttaahbt6cg539kq4k4",
                },
                input=state,
            )
            return response.output_text
        except response.RequestException as e:
            print(f"[DeepSeekClient] Ошибка запроса: {e}")
            return {"response": "..."}

    def get_npc_response(self, npc_name: str, player_pos: tuple, npc_pos: tuple, npc_text="...") -> str:
        state = jsonManager.get_value("data/npcs.json", npc_name)
        print(f"[DeepSeekClient] Полученное состояние для NPC '{npc_name}': {state}")
        if not state:
            print(f"[DeepSeekClient] NPC '{npc_name}' not found in JSON.")
            return "..."
        state["player_position"] = player_pos
        state["npc_position"] = npc_pos
        state["npc_text"] = npc_text
        result = self.send_state(state)
        result = json.loads(result)
        print(f"[DeepSeekClient] Получен ответ от NPC '{npc_name}': {result}")
        return result