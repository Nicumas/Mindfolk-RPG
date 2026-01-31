import arcade
import os
from pathlib import Path


class Player(arcade.Sprite):
    def __init__(self, x, y):
        super().__init__(scale=0.5)

        self.center_x = x
        self.center_y = y
        self.speed = 200

        self.coins = 0

        self.chatting = False

        BASE_DIR = Path(__file__).resolve().parent.parent
        TEXTURES_DIR = BASE_DIR / "textures"

        self.stand_front = arcade.load_texture(
            TEXTURES_DIR / "standing_object_front.png"
        )
        self.stand_back = arcade.load_texture(
            TEXTURES_DIR / "standing_object_back.png"
        )

        self.walk_right = arcade.load_texture(
            TEXTURES_DIR / "walk_right.png"
        )
        self.walk_left = arcade.load_texture(
            TEXTURES_DIR / "walk_left.png"
        )

        self.walk_up_left = arcade.load_texture(
            TEXTURES_DIR / "walk_up_left.png"
        )
        self.walk_up_right = arcade.load_texture(
            TEXTURES_DIR / "walk_up_right.png"
        )

        self.walk_down_left = arcade.load_texture(
            TEXTURES_DIR / "walk_down_left.png"
        )
        self.walk_down_right = arcade.load_texture(
            TEXTURES_DIR / "walk_down_right.png"
        )

        self.walk_back_right = arcade.load_texture(
            TEXTURES_DIR / "walk_back_right.png"
        )
        self.walk_forward_right = arcade.load_texture(
            TEXTURES_DIR / "walk_forward_right.png"
        )


        self.texture = self.stand_front

        self.last_direction = "down"

        base_idle_scale = 0.5
        self.idle_front_scale = base_idle_scale * 0.6
        self.idle_back_scale = base_idle_scale * 1.2

        self.walk_scale = 0.75
        self.walk_forward_scale = self.walk_scale * 0.6

        self.hit_box_points = [
            (-10, 0),
            (10, 0),
            (10, 30),
            (-10, 30),
        ]


    def update(self, dt, keys):
        if not self.chatting:
            dx = dy = 0

            if keys.get(arcade.key.W):
                dy = self.speed * dt
            if keys.get(arcade.key.S):
                dy = -self.speed * dt
            if keys.get(arcade.key.A):
                dx = -self.speed * dt
            if keys.get(arcade.key.D):
                dx = self.speed * dt

            self.change_x = dx
            self.change_y = dy


            self.update_texture(dx, dy)
        else:    
            self.change_x = 0
            self.change_y = 0


    def update_texture(self, dx, dy):
        if dx == 0 and dy == 0:
            if self.last_direction == "up":
                self.texture = self.stand_back
                self.scale = self.idle_back_scale
            else:
                self.texture = self.stand_front
                self.scale = self.idle_front_scale
            return


        self.scale = self.walk_scale

        if dx > 0 and dy > 0:
            self.texture = self.walk_up_right
            self.last_direction = "up"
        elif dx < 0 and dy > 0:
            self.texture = self.walk_up_left
            self.last_direction = "up"
        elif dx > 0 and dy < 0:
            self.texture = self.walk_down_right
            self.last_direction = "down"
        elif dx < 0 and dy < 0:
            self.texture = self.walk_down_left
            self.last_direction = "down"

        elif dx > 0:
            self.texture = self.walk_right
            self.last_direction = "right"
        elif dx < 0:
            self.texture = self.walk_left
            self.last_direction = "left"

        elif dy > 0:
            self.texture = self.walk_back_right
            self.last_direction = "up"
        elif dy < 0:
            self.texture = self.walk_forward_right
            self.scale = self.walk_forward_scale
            self.last_direction = "down"

        #self.scale = self.walk_scale

    def get_position(self):
        return (self.center_x, self.center_y)
