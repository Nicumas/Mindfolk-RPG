import arcade
from entities.npc import NPC


class Meadow:
    def __init__(self, player):
        self.player = player
        self.active_text = None

        self.player_list = arcade.SpriteList()
        self.player_list.append(player)

        self.npc_list = arcade.SpriteList()
        self.interacting_NPC = None
        self.chatting_NPC = None
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
                if npc.player_near(self.player) and self.interacting_NPC is None or self.chatting_NPC == npc:
                    npc.update_text("...думает...")
                    self.active_text = f"{npc.name}: {npc.text}"
                    npc.update_answer_async(self.player.get_position())
                    print(f"[Meadow] Взаимодействие с NPC '{npc.name}'")
                    self.interacting_NPC = npc
                    break

        for npc in self.npc_list:
            if npc.player_near(self.player):
                if npc.answer_has_been_read == False:
                    self.active_text = f"{npc.name}: {npc.get_text()}"
                    break
            else:
                if self.interacting_NPC == npc:
                    self.active_text = None
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
                40, 60,
                arcade.color.WHITE,
                16,
                width=720
            )