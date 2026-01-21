import arcade
from entities.player import Player
from scenes.meadow import Meadow

class Game(arcade.Window):
    def __init__(self):
        super().__init__(800, 600, "Mindfolk RPG")
        self.keys = {}

        self.player = Player(400, 300)
        self.scene = Meadow(self.player)

    def on_update(self, dt):
        self.scene.update(dt, self.keys)

    def on_draw(self):
        self.clear()
        self.scene.draw()

    def on_key_press(self, key, modifiers):
        self.keys[key] = True

    def on_key_release(self, key, modifiers):
        self.keys[key] = False