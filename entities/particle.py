import arcade
import random

class RunParticle(arcade.SpriteCircle):
    def __init__(self, x, y):
        super().__init__(radius=3, color=(130, 130, 130, 180))
        self.center_x = x + random.uniform(-6, 6)
        self.center_y = y + random.uniform(-6, 6)

        self.change_x = random.uniform(-20, 20)
        self.change_y = random.uniform(-10, 10)

        self.life = random.uniform(0.15, 0.30)
        self.age = 0.0

    def update(self, dt: float = 1/60):
        self.center_x += self.change_x * dt
        self.center_y += self.change_y * dt
        self.age += dt

        t = 1.0 - (self.age / self.life)
        if t <= 0:
            self.remove_from_sprite_lists()
            return

        self.alpha = int(180 * t)
        self.scale = max(0.2, t)