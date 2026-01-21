import arcade

class Meadow:
    def __init__(self, player):
        self.player_list = arcade.SpriteList()
        self.player_list.append(player)

    def update(self, dt, keys):
        for sprite in self.player_list:
            sprite.update(dt, keys)

    def draw(self):
        arcade.set_background_color(arcade.color.DARK_GREEN)
        self.player_list.draw()
