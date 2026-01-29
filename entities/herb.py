import arcade

WIDTH, HEIGHT = 800, 600
FONT_SIZE = 16

class ChatWindow(arcade.Window):
    def __init__(self):
        super().__init__(WIDTH, HEIGHT, "Chat in Arcade")
        self.input_text = ""
        self.messages = []

    def on_draw(self):
        self.clear()

        # сообщения
        y = HEIGHT - 40
        for msg in self.messages[-20:]:
            arcade.draw_text(msg, 20, y, arcade.color.WHITE, FONT_SIZE)
            y -= 20

        # строка ввода
        arcade.draw_lbwh_rectangle_filled(
            0, 0,
            self.width, 40,
            arcade.color.DARK_GRAY
        )
        arcade.draw_text(
            "> " + self.input_text,
            10, 10, arcade.color.WHITE, FONT_SIZE
        )

    def on_text(self, text):
        self.input_text += text

    def on_key_press(self, key, modifiers):
        if key == arcade.key.BACKSPACE:
            self.input_text = self.input_text[:-1]

        elif key == arcade.key.ENTER:
            if self.input_text.strip():
                self.messages.append(self.input_text)
            self.input_text = ""

if __name__ == "__main__":
    ChatWindow()
    arcade.run()
