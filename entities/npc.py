import arcade
import math
import threading
from pathlib import Path



from ai.deepseek_client import DeepSeekClient


class NPC(arcade.Sprite):
    def __init__(
        self,
        x: float,
        y: float,
        name: str = "villager",
        text: str = "*Нажмите E, чтобы поговорить",
        scale: float = 1.0
    ):
        BASE_DIR = Path(__file__).resolve().parent.parent
        TEXTURES_DIR = BASE_DIR / "textures"

        texture_file = TEXTURES_DIR / "villager_npc.png"
        if not texture_file.exists():
            raise FileNotFoundError(f"Не найден файл текстуры: {texture_file}")

        texture = arcade.load_texture(texture_file)

        super().__init__()
        self.texture = texture

        self.scale = scale * 0.8

        self.center_x = x
        self.center_y = y

        self.coins = 0

        self.name = name
        self.text = text
        self.answer_has_been_read = False
        self.interact_distance = 80

        self.stand_texture = texture

    def player_near(self, player) -> bool:
        dx = self.center_x - player.center_x
        dy = self.center_y - player.center_y
        return math.hypot(dx, dy) <= self.interact_distance

    def update_text(self, new_text: str):
        self.text = new_text
        print(f"[NPC] Текст NPC '{self.name}' обновлён: {self.text}")

    def get_position(self):
        return self.center_x, self.center_y

    def get_name(self):  
        return self.name
    
    def get_coins(self):
        coins = self.coins
        self.coins = 0
        return coins

    def get_text(self):
        self.answer_has_been_read = True
        return self.text

    def update_answer_async(self, player_pos):
        thread = threading.Thread(
            target=self._fetch_answer,
            args=(player_pos,),
            daemon=True
        )
        thread.start()

    def _fetch_answer(self, player_pos):
        try:
            client = DeepSeekClient()
            response = client.get_npc_response(
                npc_name=self.name,
                player_pos=player_pos,
                npc_pos=self.get_position(),
                npc_text=self.get_text()
            )
            print(f"[NPC] Получен ответ от NPC '{self.name}': {response}")
            self.text = response["answer"]
            self.coins = response["coins"]
            print(f"[NPC] Получен ответ от NPC, монет: {self.coins}")
            self.answer_has_been_read = False

        except Exception as e:
            print(f"[NPC ERROR] {e}")