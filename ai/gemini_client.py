import requests
import json
import re
from data.json_manager import jsonManager

GOOGLE_GEMINI_URL = jsonManager.get_value("data/data.json", "api_google")["GOOGLE_GEMINI_URL"]

NPC_SCHEMA = {
    "type": "object",
    "required": [
        "answer", "action", "coins", "emotion", "quest",
        "trust", "aggression", "relationship", "memory_note", "next_state"
    ],
    "properties": {
        "trust": {"type": "integer", "minimum": 0, "maximum": 100},
        "next_state": {"type": "string"},
        "emotion": {"type": "string", "enum": ["calm", "happy", "angry", "afraid", "sad"]},
        "answer": {"type": "string"},
        "coins": {"type": "integer"},
        "name": {"type": "string"},
        "action": {"type": "string", "enum": ["talk", "give_coins", "give_quest", "trade", "attack", "ignore"]},
        "aggression": {"type": "integer", "minimum": 0, "maximum": 100},
        "relationship": {"type": "string", "enum": ["friendly", "neutral", "hostile"]},
        "quest": {
            "type": ["object", "null"],
            "required": ["id", "title", "goal", "reward_coins"],
            "properties": {
                "reward_coins": {"type": "integer"},
                "goal": {"type": "string"},
                "id": {"type": "string"},
                "title": {"type": "string"}
            }
        },
        "memory_note": {"type": "string"}
    }
}

def _extract_json(text: str) -> str:
    t = (text or "").strip()
    if t.startswith("{") and t.endswith("}"):
        return t
    m = re.search(r"\{.*\}", t, flags=re.DOTALL)
    return m.group(0) if m else ""

def _fallback_result() -> dict:
    return {
        "answer": "...",
        "action": "talk",
        "coins": 0,
        "emotion": "calm",
        "quest": None,
        "trust": 50,
        "aggression": 0,
        "relationship": "neutral",
        "memory_note": "",
        "next_state": ""
    }

def _validate(obj: dict) -> bool:
    for k in NPC_SCHEMA["required"]:
        if k not in obj:
            return False

    if obj["emotion"] not in ["calm", "happy", "angry", "afraid", "sad"]:
        return False
    if obj["action"] not in ["talk", "give_coins", "give_quest", "trade", "attack", "ignore"]:
        return False
    if obj["relationship"] not in ["friendly", "neutral", "hostile"]:
        return False

    if not isinstance(obj["trust"], int) or obj["trust"] < 0 or obj["trust"] > 100:
        return False
    if not isinstance(obj["aggression"], int) or obj["aggression"] < 0 or obj["aggression"] > 100:
        return False
    if not isinstance(obj["coins"], int):
        return False
    if not isinstance(obj["answer"], str):
        return False
    if not isinstance(obj["memory_note"], str):
        return False
    if not isinstance(obj["next_state"], str):
        return False

    q = obj["quest"]
    if q is not None:
        if not isinstance(q, dict):
            return False
        for rk in ["id", "title", "goal", "reward_coins"]:
            if rk not in q:
                return False
        if not isinstance(q["reward_coins"], int):
            return False
        if not isinstance(q["id"], str) or not isinstance(q["title"], str) or not isinstance(q["goal"], str):
            return False

    return True

class GeminiClient:
    def __init__(self):
        self.url = GOOGLE_GEMINI_URL

    def send_state(self, state: dict) -> dict:
        schema_text = json.dumps(NPC_SCHEMA, ensure_ascii=False)

        instruction = (
            "Ты — NPC в игре. Верни ответ СТРОГО в формате JSON.\n"
            "Никакого текста до или после JSON.\n"
            "JSON должен соответствовать следующей JSON Schema:\n"
            f"{schema_text}\n"
            "Если квеста нет — quest = null.\n"
        )

        payload = {
            "contents": [
                {
                    "parts": [
                        {"text": instruction + "\nСостояние:\n" + json.dumps(state, ensure_ascii=False)}
                    ]
                }
            ]
        }

        try:
            r = requests.post(self.url, json=payload, timeout=30)
            data = r.json()
        except Exception as e:
            print(f"[GeminiClient] Ошибка запроса: {e}")
            return _fallback_result()

        if "candidates" not in data:
            print("[GeminiClient] Ошибка от API:", data)
            return _fallback_result()

        text = data["candidates"][0]["content"]["parts"][0].get("text", "")
        raw_json = _extract_json(text)

        if not raw_json:
            print("[GeminiClient] Не нашёл JSON в ответе:", text)
            return _fallback_result()

        try:
            obj = json.loads(raw_json)
        except Exception as e:
            print(f"[GeminiClient] JSON parse error: {e}")
            print("[GeminiClient] Raw:", raw_json)
            return _fallback_result()

        if not isinstance(obj, dict) or not _validate(obj):
            print("[GeminiClient] Неверная структура ответа:", obj)
            return _fallback_result()

        return obj

    def get_npc_response(self, npc_name: str, player_pos: tuple, npc_pos: tuple, npc_text="...") -> dict:
        state = jsonManager.get_value("data/npcs.json", npc_name)
        print(f"[GeminiClient] Полученное состояние для NPC '{npc_name}': {state}")

        if not state:
            print(f"[GeminiClient] NPC '{npc_name}' not found in JSON.")
            return _fallback_result()

        if npc_text == "...думает...":
            npc_text = "*К вам подошел игрок"

        state["player_position"] = player_pos
        state["npc_position"] = npc_pos
        state["answer"] = npc_text

        print(f"[GeminiClient] Отправляемое состояние для NPC '{npc_name}': {state}")

        result = self.send_state(state)
        print(f"[GeminiClient] Ответ от сервера для NPC '{npc_name}': {result}")

        answer = result.get("answer", "...")
        result_for_save = result.copy()
        result_for_save["answer"] = ""

        print(f"[For save] Отправляемое состояние для {npc_name}': {result_for_save}")
        jsonManager.update_json("data/npcs.json", npc_name, result_for_save)

        result["answer"] = answer
        return result