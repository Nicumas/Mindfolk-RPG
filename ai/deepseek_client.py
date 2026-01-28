import requests
import json

class DeepSeekClient:
    def __init__(self, base_url: str):
        self.base_url = base_url.rstrip("/")

    def send_state(self, state: dict) -> dict:
        try:
            response = requests.post(
                f"{self.base_url}/query",
                headers={"Content-Type": "application/json"},
                data=json.dumps(state),
                timeout=5
            )
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            print(f"[DeepSeekClient] Ошибка запроса: {e}")
            return {"response": "..."}

    def get_npc_response(self, npc_name: str, player_pos: tuple, npc_pos: tuple) -> str:
        state = {
            "npc_name": npc_name,
            "player_pos": {"x": player_pos[0], "y": player_pos[1]},
            "npc_pos": {"x": npc_pos[0], "y": npc_pos[1]},
        }
        result = self.send_state(state)
        return result.get("response", "...")
