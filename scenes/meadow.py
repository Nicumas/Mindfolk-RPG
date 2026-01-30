import arcade
from entities.npc import NPC

FONT_SIZE = 16

class Meadow:
    def __init__(self, player):
        self.player = player
        self.active_text = None

        self.player_list = arcade.SpriteList()
        self.player_list.append(player)

        self.active_text_lines = []  # список строк текста NPC
        self.chat_scroll = 0         # индекс верхней видимой строки
        MAX_LINES = 6  

        self.npc_list = arcade.SpriteList()
        self.interacting_NPC = None
        self.input_text = ""
        self.npc_list.append(
            NPC(500, 300, "villager")
        )

        self.setup()

    def setup(self):
        TILE_SCALING = 0.4
        tile_map = arcade.load_tilemap("textures/layer1.tmx", scaling=TILE_SCALING)

        self.world_width = int(tile_map.width * tile_map.tile_width * TILE_SCALING)
        self.world_height = int(tile_map.height * tile_map.tile_height * TILE_SCALING)

        self.terra_list = tile_map.sprite_lists["terra"]
        self.collision_list = tile_map.sprite_lists["collision"]

    def update(self, dt, keys):
        self.player.update(dt, keys)

        if keys.get(arcade.key.E):
            for npc in self.npc_list:
                if npc.player_near(self.player) and self.interacting_NPC is None or self.player.chatting == False:
                    npc.update_text("...думает...")
                    self.set_active_text(f"{npc.name}: {npc.text}")
                    npc.update_answer_async(self.player.get_position())
                    print(f"[Meadow] Взаимодействие с NPC '{npc.name}'")
                    self.interacting_NPC = npc
                    self.player.chatting = True
                    break

        for npc in self.npc_list:

            # Пример прокрутки при нажатии стрелок
            if keys.get(arcade.key.UP):
                self.scroll_chat(-1)
            if keys.get(arcade.key.DOWN):
                self.scroll_chat(1)

            if npc.player_near(self.player):
                if npc.answer_has_been_read == False:
                    self.set_active_text(f"{npc.name}: {npc.text}")
                    self.interacting_NPC = npc
                    break
            else:
                self.active_text = None
                self.input_text = ""
                self.player.chatting = False
                if self.interacting_NPC == npc:
                    self.interacting_NPC = None

    def draw_world(self):
        self.terra_list.draw()
        self.npc_list.draw()
        self.player_list.draw()

    def draw_gui(self):
        # блок текста NPC
        if self.active_text_lines:
            arcade.draw_lrbt_rectangle_filled(
                20, 780,
                30, 120,  # высота блока чата
                arcade.color.BLACK
            )
            start_line = self.chat_scroll
            end_line = start_line + self.MAX_LINES
            visible_lines = self.active_text_lines[start_line:end_line]
            for i, line in enumerate(visible_lines):
                arcade.draw_text(
                    line,
                    40, 120 - 20 - i * (FONT_SIZE + 2),
                    arcade.color.WHITE,
                    FONT_SIZE,
                    width=720
                )

        # блок ввода
        arcade.draw_lbwh_rectangle_filled(
            20, 0,
            760, 40,
            arcade.color.DARK_GRAY
        )
        arcade.draw_text(
            "> " + self.input_text,
            30, 10, arcade.color.WHITE, FONT_SIZE
        )

    def on_text(self, text):
        if self.player.chatting:
            self.input_text += text

    def set_active_text(self, text):
        self.active_text_lines = arcade.get_lines(text, FONT_SIZE, 720)
        self.chat_scroll = 0

    def scroll_chat(self, direction):
        """ direction = 1 вниз, -1 вверх """
        if not self.active_text_lines:
            return
        self.chat_scroll += direction
        self.chat_scroll = max(0, min(self.chat_scroll, len(self.active_text_lines) - self.MAX_LINES))

    def chat_with_npc(self, npc, message):
        pass