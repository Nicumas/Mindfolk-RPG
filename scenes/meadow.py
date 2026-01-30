import arcade
from entities.npc import NPC

FONT_SIZE = 16

class Meadow:
    def __init__(self, player):
        self.player = player
        self.active_text = None

        self.player_list = arcade.SpriteList()
        self.player_list.append(player)

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
                    self.active_text = f"{npc.name}: {npc.text}"
                    npc.update_answer_async(self.player.get_position())
                    print(f"[Meadow] Взаимодействие с NPC '{npc.name}'")
                    self.interacting_NPC = npc
                    self.player.chatting = True
                    break

        for npc in self.npc_list:
            if npc.player_near(self.player):
                if npc.answer_has_been_read == False:
                    self.active_text = f"{npc.name}: {npc.get_text()}"
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
        if self.active_text:
            arcade.draw_lrbt_rectangle_filled(
                20, 780,
                30, 130,
                arcade.color.BLACK
            )
            arcade.draw_text(
                self.active_text,
                40, 90,
                arcade.color.WHITE,
                16,
                width=720
            )
            # строка ввода
            arcade.draw_lbwh_rectangle_filled(
                0, 0,
                720, 40,
                arcade.color.DARK_GRAY
            )
            arcade.draw_text(
                "> " + self.input_text,
                10, 10, arcade.color.WHITE, FONT_SIZE
            )

    def on_text(self, text):
        if self.player.chatting:
            self.input_text += text

    def chat_with_npc(self, npc, message):
        pass