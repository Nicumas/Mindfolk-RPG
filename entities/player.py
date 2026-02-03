import arcade
from pathlib import Path
from entities.particle import RunParticle


class Player(arcade.Sprite):
    def __init__(self, x, y, particles_list: arcade.SpriteList):
        super().__init__(scale=0.5)

        self.particles_list = particles_list
        self.particle_timer = 0.0
        self.particle_interval = 0.03

        self.center_x = x
        self.center_y = y
        self.speed = 200

        self.coins = 0
        self.max_hp = 100
        self.hp = self.max_hp
        self.damage = 20
        self.dead = False

        self.chatting = False

        BASE_DIR = Path(__file__).resolve().parent.parent
        TEXTURES_DIR = BASE_DIR / "textures"

        self.stand_front = arcade.load_texture(TEXTURES_DIR / "standing_object_front.png")
        self.stand_back = arcade.load_texture(TEXTURES_DIR / "standing_object_back.png")

        self.walk_right = arcade.load_texture(TEXTURES_DIR / "walk_right.png")
        self.walk_left = arcade.load_texture(TEXTURES_DIR / "walk_left.png")

        self.walk_up_left = arcade.load_texture(TEXTURES_DIR / "walk_up_left.png")
        self.walk_up_right = arcade.load_texture(TEXTURES_DIR / "walk_up_right.png")

        self.walk_down_left = arcade.load_texture(TEXTURES_DIR / "walk_down_left.png")
        self.walk_down_right = arcade.load_texture(TEXTURES_DIR / "walk_down_right.png")

        self.walk_back_right = arcade.load_texture(TEXTURES_DIR / "walk_back_right.png")
        self.walk_forward_right = arcade.load_texture(TEXTURES_DIR / "walk_forward_right.png")

        self.texture = self.stand_front
        self.last_direction = "down"

        base_idle_scale = 0.5
        self.idle_front_scale = base_idle_scale * 0.6
        self.idle_back_scale = base_idle_scale * 1.2

        self.walk_scale = 0.75
        self.walk_forward_scale = self.walk_scale * 0.6

        self.hit_box_points = [(-10, 0), (10, 0), (10, 30), (-10, 30)]

    def check_dead(self):
        if self.hp == 0:
            self.dead = True

    def update(self, dt, keys):
        self.check_dead()

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
            self.update_run_particles(dt, dx, dy)
        else:
            self.change_x = 0
            self.change_y = 0

    def update_run_particles(self, dt, dx, dy):
        moving = (dx != 0 or dy != 0)
        if not moving:
            self.particle_timer = 0.0
            return

        self.particle_timer += dt
        while self.particle_timer >= self.particle_interval:
            self.particle_timer -= self.particle_interval

            if self.last_direction == "up":
                px = self.center_x
                py = self.center_y - 6
            elif self.last_direction == "down":
                px = self.center_x
                py = self.center_y - 14
            elif self.last_direction == "left":
                px = self.center_x + 8
                py = self.center_y - 12
            else:
                px = self.center_x - 8
                py = self.center_y - 12

            self.particles_list.append(RunParticle(px, py))

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

    def get_position(self):
        return (self.center_x, self.center_y)

    def take_damage(self, dmg):
        self.hp -= dmg
        if self.hp < 0:
            self.hp = 0

    def attack(self):
        pass
