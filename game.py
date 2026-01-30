import arcade
from entities.player import Player
from scenes.meadow import Meadow

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

DEAD_ZONE_W = int(SCREEN_WIDTH * 0.15)
DEAD_ZONE_H = int(SCREEN_HEIGHT * 0.15)

CAMERA_LERP = 0.1


class Game(arcade.Window):
    def __init__(self):
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, "Mindfolk RPG")
        self.keys = {}

        self.world_camera = arcade.camera.Camera2D()
        self.gui_camera = arcade.camera.Camera2D()

        self.camera_shake = arcade.camera.grips.ScreenShake2D(
            self.world_camera.view_data,
            max_amplitude=15.0,
            acceleration_duration=0.1,
            falloff_time=0.5,
            shake_frequency=10.0,
        )

        self.player = Player(400, 300)
        self.scene = Meadow(self.player)
        self.world_width = self.scene.world_width
        self.world_height = self.scene.world_height

    def on_update(self, dt):
        self.scene.update(dt, self.keys)

        self.camera_shake.update(dt)

        cam_x, cam_y = self.world_camera.position
        dz_left = cam_x - DEAD_ZONE_W // 2
        dz_right = cam_x + DEAD_ZONE_W // 2
        dz_bottom = cam_y - DEAD_ZONE_H // 2
        dz_top = cam_y + DEAD_ZONE_H // 2

        px, py = self.player.center_x, self.player.center_y
        target_x, target_y = cam_x, cam_y

        if px < dz_left:
            target_x = px + DEAD_ZONE_W // 2
        elif px > dz_right:
            target_x = px - DEAD_ZONE_W // 2
        if py < dz_bottom:
            target_y = py + DEAD_ZONE_H // 2
        elif py > dz_top:
            target_y = py - DEAD_ZONE_H // 2

        half_w = self.world_camera.viewport_width / 2
        half_h = self.world_camera.viewport_height / 2
        target_x = max(half_w, min(self.world_width - half_w, target_x))
        target_y = max(half_h, min(self.world_height - half_h, target_y))

        smooth_x = (1 - CAMERA_LERP) * cam_x + CAMERA_LERP * target_x
        smooth_y = (1 - CAMERA_LERP) * cam_y + CAMERA_LERP * target_y
        self.cam_target = (smooth_x, smooth_y)
        
        self.world_camera.position = (self.cam_target[0], self.cam_target[1])
        

    def on_draw(self):
        self.clear()

        self.world_camera.use()
        self.camera_shake.update_camera()
        self.scene.draw_world()
        self.camera_shake.readjust_camera()

        self.gui_camera.use()
        self.scene.draw_gui()

    def on_text(self, text):
        if self.player.chatting: 
            self.scene.input_text += text
            print(f"Текущий ввод: {self.scene.input_text}")

    def on_key_press(self, key, modifiers):
        self.keys[key] = True

        if self.player.chatting and self.scene.interacting_NPC.get_text():
            if key == arcade.key.BACKSPACE:
                self.scene.input_text = self.scene.input_text[:-1]

            elif key == arcade.key.ENTER:
                if self.scene.input_text.strip():
                    self.scene.interacting_NPC.update_text("...думает...")
                    self.scene.active_text = f"{self.scene.interacting_NPC.name}: {self.scene.interacting_NPC.text}"
                    self.scene.interacting_NPC.update_text(self.scene.input_text)
                    self.scene.interacting_NPC.update_answer_async(self.player.get_position())
                self.scene.input_text = ""

    def on_key_release(self, key, modifiers):
        self.keys[key] = False