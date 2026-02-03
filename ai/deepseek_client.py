import openai
from data.json_manager import jsonManager
import json

YANDEX_CLOUD_FOLDER = jsonManager.get_value("data/data.json", "api_yandex")["YANDEX_CLOUD_FOLDER"]
YANDEX_CLOUD_API_KEY = jsonManager.get_value("data/data.json", "api_yandex")["YANDEX_CLOUD_API_KEY"]

class DeepSeekClient:
    def __init__(self):
        self.client = openai.OpenAI(
            api_key=YANDEX_CLOUD_API_KEY,
            base_url="https://rest-assistant.api.cloud.yandex.net/v1",
            project=YANDEX_CLOUD_FOLDER
        )

    def send_state(self, state_json: str) -> str:
        try:
            resp = self.client.responses.create(
                prompt={"id": "fvttaahbt6cg539kq4k4"},
                input=state_json,
            )
            return getattr(resp, "output_text", "") or ""
        except Exception as e:
            print(f"[DeepSeekClient] Ошибка запроса: {e}")
            return "{}"

    def get_npc_response(self, npc_name: str, player_pos: tuple, npc_pos: tuple, npc_text="...") -> dict:
        state = jsonManager.get_value("data/npcs.json", npc_name)
        print(f"[DeepSeekClient] Полученное состояние для NPC '{npc_name}': {state}")

        if not state:
            print(f"[DeepSeekClient] NPC '{npc_name}' not found in JSON.")
            return {"answer": "..."}

        if npc_text == "...думает...":
            npc_text = "*К вам подошел игрок"

        state["player_position"] = player_pos
        state["npc_position"] = npc_pos
        state["answer"] = npc_text

        print(f"[DeepSeekClient] Отправляемое состояние для NPC '{npc_name}': {state}")
        state_json = json.dumps(state, ensure_ascii=False)

        raw = self.send_state(state_json)
        print(f"[DeepSeekClient] Ответ от сервера для NPC '{npc_name}': {raw}")

        try:
            result = json.loads(raw) if isinstance(raw, str) else raw
        except Exception as e:
            print(f"[DeepSeekClient] Не смог распарсить JSON: {e}")
            return {"answer": "..."}

        if not isinstance(result, dict):
            print(f"[DeepSeekClient] Сервер вернул не dict: {type(result)}")
            return {"answer": "..."}

        answer = result.get("answer", "...")

        result_for_save = result.copy()
        result_for_save["answer"] = ""
        print(f"[For save] Отправляемое состояние для {npc_name}': {result_for_save}")

        jsonManager.update_json("data/npcs.json", npc_name, result_for_save)

        result["answer"] = answer
        return result