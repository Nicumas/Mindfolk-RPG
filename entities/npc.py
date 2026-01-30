import arcade
import math
import threading
from ai.deepseek_client import DeepSeekClient


class NPC(arcade.SpriteSolidColor):
    def __init__(self, x, y, name="villager", text="*Нажмите E, чтобы поговорить"):
        super().__init__(32, 32, arcade.color.BROWN)
        self.center_x = x
        self.center_y = y

        self.name = name
        self.text = text
        self.answer_has_been_read = False
        self.interact_distance = 80

    def player_near(self, player):
        dx = self.center_x - player.center_x
        dy = self.center_y - player.center_y
        return math.hypot(dx, dy) <= self.interact_distance

    def update_text(self, new_text):
        self.text = new_text
        print(f"[NPC] Текст NPC '{self.name}' обновлён: {self.text}")

    def get_position(self):
        return (self.center_x, self.center_y)

    def get_name(self):
        return self.name

    def get_text(self):
        self.answer_has_been_read = True
        return self.text

    def update_answer_async(self, player_pos):
        threading.Thread(target=self._fetch_answer, args=(player_pos,), daemon=True).start()

    def _fetch_answer(self, player_pos):
        client = DeepSeekClient()
        response = client.get_npc_response(
            npc_name=self.name,
            player_pos=player_pos,
            npc_pos=self.get_position(),
            npc_text=self.get_text()
        )

        print(f"[NPC] Получен ответ от NPC '{self.name}': {response}")
        self.text = response["answer"]
        self.answer_has_been_read = False