import arcade

class Player(arcade.SpriteSolidColor):
    def __init__(self, x, y):
        super().__init__(32, 32, arcade.color.BLUE)
        self.center_x = x
        self.center_y = y
        self.speed = 200

    def update(self, dt, keys):
        if keys.get(arcade.key.W):
            self.center_y += self.speed * dt
        if keys.get(arcade.key.S):
            self.center_y -= self.speed * dt
        if keys.get(arcade.key.A):
            self.center_x -= self.speed * dt
        if keys.get(arcade.key.D):
            self.center_x += self.speed * dt

    def get_position(self):
        return (self.center_x, self.center_y)