import arcade
from entities.npc import NPC
import textwrap

FONT_SIZE = 16
MAX_LINES = 6  

class Meadow:
    def __init__(self, player):
        self.player = player
        self.active_text = None

        self.player_list = arcade.SpriteList()
        self.player_list.append(player)

        self.active_text_lines = []
        self.chat_scroll = 0 

        self.npc_list = arcade.SpriteList()
        self.interacting_NPC = None
        self.input_text = ""
        self.npc_list.append(
            NPC(500, 300, "villager")
        )
        #self.npc_list.append(
        #    NPC(500, 400, "Guard")
        #)

        self.setup()

    def setup(self):
        TILE_SCALING = 0.4
        tile_map = arcade.load_tilemap("textures/layer1.tmx", scaling=TILE_SCALING)

        self.world_width = int(tile_map.width * tile_map.tile_width * TILE_SCALING)
        self.world_height = int(tile_map.height * tile_map.tile_height * TILE_SCALING)

        self.terra_list = tile_map.sprite_lists["terra"]
        self.collision_list = tile_map.sprite_lists["collision"]

        self.physics_engine = arcade.PhysicsEngineSimple(
            self.player,
            self.collision_list
        )

    def update(self, dt, keys):
        self.player.update(dt, keys)
        self.physics_engine.update()

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
            if keys.get(arcade.key.UP):
                self.scroll_chat(-1)
                print(1111111)
            if keys.get(arcade.key.DOWN):
                self.scroll_chat(1)
                print(1111111)

            if keys.get(arcade.key.ESCAPE):
                self.hide_chat()

            if npc.player_near(self.player):
                if npc.answer_has_been_read == False:
                    self.set_active_text(f"{npc.name}: {npc.text}")
                    self.interacting_NPC = npc
                    break
            else:
                self.hide_chat()

    def draw_world(self):
        self.terra_list.draw()
        self.npc_list.draw()
        self.player_list.draw()

    def draw_gui(self):
        if self.active_text_lines:
            arcade.draw_lrbt_rectangle_filled(
                20, 780,
                30, 120, 
                arcade.color.BLACK
            )
            start_line = self.chat_scroll
            end_line = start_line + MAX_LINES
            visible_lines = self.active_text_lines[start_line:end_line]
            for i, line in enumerate(visible_lines):
                arcade.draw_text(
                    line,
                    40, 120 - 20 - i * (FONT_SIZE + 2),
                    arcade.color.WHITE,
                    FONT_SIZE,
                    width=720
                )

            arcade.draw_lbwh_rectangle_filled(
                20, 0,
                760, 40,
                arcade.color.DARK_GRAY
            )
            if self.input_text == "" and self.interacting_NPC.answer_has_been_read == True:
                arcade.draw_text(
                    "> " + "Начните что то писать, ESC - чтобы выйти из чата.",
                    30, 10, arcade.color.WHITE, FONT_SIZE
                )
            else:
                arcade.draw_text(
                    "> " + self.input_text,
                    30, 10, arcade.color.WHITE, FONT_SIZE
                )

    def on_text(self, text):
        if self.player.chatting:
            self.input_text += text

    def set_active_text(self, text):
        chars_per_line = 70
        self.active_text_lines = textwrap.wrap(text, chars_per_line)
        self.chat_scroll = 0


    def scroll_chat(self, direction):
        if not self.active_text_lines:
            return
        self.chat_scroll += direction
        self.chat_scroll = max(0, min(self.chat_scroll, len(self.active_text_lines) - MAX_LINES))

    def hide_chat(self):
        if not self.interacting_NPC is None:
            self.interacting_NPC.answer_has_been_read = False
            self.interacting_NPC.update_text("*Нажмите E, чтобы поговорить")
        self.active_text_lines = []
        self.chat_scroll = 0
        self.input_text = ""
        self.player.chatting = False
        self.interacting_NPC = None

    def chat_with_npc(self, npc, message):
        pass