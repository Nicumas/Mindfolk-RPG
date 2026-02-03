import arcade
import math

class Mob(arcade.Sprite):
    def __init__(self, x, y, texture_path, scale=1.0):
        super().__init__(texture_path, scale=scale)
        self.center_x = x
        self.center_y = y

        self.max_hp = 30
        self.hp = self.max_hp

        self.speed = 120.0
        self.aggro_radius = 220.0
        self.attack_radius = 28.0

        self.damage = 5
        self.attack_cooldown = 0.8
        self._attack_timer = 0.0

        self.patrol_points = [(x - 80, y), (x + 80, y)]
        self._patrol_i = 0
        self._target_x, self._target_y = self.patrol_points[self._patrol_i]

        self.alive = True

    def distance_to(self, x, y):
        dx = x - self.center_x
        dy = y - self.center_y
        return math.hypot(dx, dy)

    def _move_towards(self, tx, ty, dt):
        dx = tx - self.center_x
        dy = ty - self.center_y
        dist = math.hypot(dx, dy)
        if dist < 1e-6:
            return

        vx = (dx / dist) * self.speed
        vy = (dy / dist) * self.speed
        self.center_x += vx * dt
        self.center_y += vy * dt

    def take_damage(self, amount):
        if not self.alive:
            return
        self.hp -= amount
        if self.hp <= 0:
            self.hp = 0
            self.alive = False
            self.remove_from_sprite_lists()

    def update_ai(self, dt, player, walls=None):
        if not self.alive:
            return

        self._attack_timer = max(0.0, self._attack_timer - dt)

        px, py = player.center_x, player.center_y
        dist = self.distance_to(px, py)

        # 1) если игрок рядом — преследуем
        if dist <= self.aggro_radius:
            old_x, old_y = self.center_x, self.center_y
            self._move_towards(px, py, dt)

            # коллизии со стенами (если передали список стен)
            if walls is not None and arcade.check_for_collision_with_list(self, walls):
                self.center_x, self.center_y = old_x, old_y

            # атака по радиусу и кулдауну
            if dist <= self.attack_radius and self._attack_timer <= 0.0:
                if hasattr(player, "take_damage"):
                    player.take_damage(self.damage)
                self._attack_timer = self.attack_cooldown
            return

        # 2) иначе — патруль между точками
        tx, ty = self._target_x, self._target_y
        if self.distance_to(tx, ty) < 8:
            self._patrol_i = (self._patrol_i + 1) % len(self.patrol_points)
            self._target_x, self._target_y = self.patrol_points[self._patrol_i]
            tx, ty = self._target_x, self._target_y

        old_x, old_y = self.center_x, self.center_y
        self._move_towards(tx, ty, dt)
        if walls is not None and arcade.check_for_collision_with_list(self, walls):
            self.center_x, self.center_y = old_x, old_y