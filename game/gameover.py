import arcade

import mainmenu


class GameOver(arcade.View):
    def __init__(self):
        super().__init__()
        self.gameover = arcade.Text(
            "Game Over!",
            self.window.width / 2,
            self.window.height / 2,
            anchor_x="center",
            anchor_y="bottom",
            font_name="PressStart2P",
            font_size=28,
        )
        self.stopwatch = 0
        self.press_enter = arcade.Text(
            "Press ENTER to return to the main menu",
            self.window.width / 2,
            self.window.height / 2 - 20,
            anchor_x="center",
            anchor_y="top",
            font_name="PressStart2P",
            font_size=14,
        )
        self.show_press_enter = False

    def on_key_press(self, symbol: int, modifiers: int):
        if symbol == arcade.key.ENTER:
            if self.show_press_enter:
                self.window.show_view(mainmenu.MainMenu())
            else:
                self.show_press_enter = True

        return super().on_key_press(symbol, modifiers)

    def on_update(self, delta_time: float):
        self.stopwatch += delta_time
        if not self.show_press_enter and self.stopwatch > 2:
            self.show_press_enter = True

    def on_draw(self):
        self.gameover.draw()
        if self.show_press_enter:
            self.press_enter.draw()
