import arcade
import os

class Player(arcade.Sprite):
    def __init__(self, x, y):
        super().__init__()

        self.center_x = x
        self.center_y = y
        self.speed = 200

        # Списки для кадров анимации
        self.idle_textures = [""]
        self.walk_textures = []

        # Текущее состояние
        self.cur_texture = 0
        self.facing_right = True
        self.state = "idle"  # "idle" или "walk"

        # Загружаем текстуры
        self.load_textures()

        # Устанавливаем стартовую текстуру
        self.texture = self.idle_textures[0]

    def load_textures(self):
        """Загрузка кадров анимации"""
        # Папка с картинками
        folder = "images/player"

        # Загрузка idle кадров
        for i in range(1, 3):  # допустим у тебя 2 кадра idle
            texture = arcade.load_texture(os.path.join(folder, f"idle_{i}.png"))
            self.idle_textures.append(texture)

        # Загрузка walk кадров
        for i in range(1, 5):  # допустим 4 кадра ходьбы
            texture = arcade.load_texture(os.path.join(folder, f"walk_{i}.png"))
            self.walk_textures.append(texture)

    def update(self, dt, keys):
        dx = dy = 0
        if keys.get(arcade.key.W):
            dy = self.speed * dt
        if keys.get(arcade.key.S):
            dy = -self.speed * dt
        if keys.get(arcade.key.A):
            dx = -self.speed * dt
            self.facing_right = False
        if keys.get(arcade.key.D):
            dx = self.speed * dt
            self.facing_right = True

        self.center_x += dx
        self.center_y += dy

        # Определяем состояние
        if dx != 0 or dy != 0:
            self.state = "walk"
        else:
            self.state = "idle"

        # Обновляем текстуру
        self.update_animation(dt)

    def update_animation(self, dt):
        if self.state == "idle":
            textures = self.idle_textures
        elif self.state == "walk":
            textures = self.walk_textures

        # Меняем кадр каждые 0.15 секунд
        self.cur_texture += 1
        if self.cur_texture >= len(textures) * 6:  # 6 кадров = 0.15 сек при 60 fps
            self.cur_texture = 0

        frame = self.cur_texture // 6
        texture = textures[frame]

        # Поворачиваем текстуру если идём влево
        if not self.facing_right:
            texture = arcade.load_texture(texture.path, mirrored=True)

        self.texture = texture
