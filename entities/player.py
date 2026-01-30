import arcade
import os
from pathlib import Path


class Player(arcade.Sprite):
    def __init__(self, x, y):
        # Базовый масштаб — для стоячих спрайтов
        super().__init__(scale=0.5)

        self.center_x = x
        self.center_y = y
        self.speed = 200

        self.chatting = False

        BASE_DIR = Path(__file__).resolve().parent.parent
        TEXTURES_DIR = BASE_DIR / "textures"

        # --- Idle ---
        self.stand_front = arcade.load_texture(
            TEXTURES_DIR / "standing_object_front.png"
        )
        self.stand_back = arcade.load_texture(
            TEXTURES_DIR / "standing_object_back.png"
        )

        # --- Walk ---
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


        # Начальная текстура — idle
        self.texture = self.stand_front
        self.last_direction = "down"

        # Масштабы для разных состояний
        self.idle_scale = 0.5
        self.walk_scale = 0.75

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

            self.center_x += dx
            self.center_y += dy

            self.update_texture(dx, dy)

    def update_texture(self, dx, dy):
        # Стоим на месте
        if dx == 0 and dy == 0:
            self.scale = self.idle_scale
            if self.last_direction == "up":
                self.texture = self.stand_back
            else:
                self.texture = self.stand_front
            return

        # Движение — увеличиваем масштаб
        self.scale = self.walk_scale

        # Диагонали
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

        # Горизонталь
        elif dx > 0:
            self.texture = self.walk_right
            self.last_direction = "right"
        elif dx < 0:
            self.texture = self.walk_left
            self.last_direction = "left"

        # Вертикаль
        elif dy > 0:
            self.texture = self.walk_back_right
            self.last_direction = "up"
        elif dy < 0:
            self.texture = self.walk_forward_right
            self.last_direction = "down"

    def get_position(self):
        return (self.center_x, self.center_y)
