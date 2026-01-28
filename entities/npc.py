import arcade
import math

class NPC(arcade.SpriteSolidColor):
    def __init__(self, x, y, name="Villager", text="Привет, путник!"):
        super().__init__(32, 32, arcade.color.BROWN)
        self.center_x = x
        self.center_y = y

        self.name = name
        self.text = text
        self.interact_distance = 80

    def player_near(self, player):
        dx = self.center_x - player.center_x
        dy = self.center_y - player.center_y
        return math.hypot(dx, dy) <= self.interact_distance