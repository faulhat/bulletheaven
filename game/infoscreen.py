import arcade

from stopwatch import GameObject


class InfoScreen(arcade.View, GameObject):
    def __init__(
        self,
        labels: list[arcade.Text],
        press_enter: arcade.Text,
        next_view: arcade.View,
    ):
        GameObject.__init__(self)
        arcade.View.__init__(self)
        self.labels = labels
        self.show_press_enter = False
        self.press_enter = press_enter
        self.next_view = next_view
        self.press_enter_clock = self.new_stopwatch()

    def on_key_press(self, symbol: int, modifiers: int):
        if symbol == arcade.key.ENTER:
            if self.show_press_enter:
                self.window.show_view(self.next_view)
            else:
                self.show_press_enter = True

        return super().on_key_press(symbol, modifiers)

    def on_update(self, delta_time: float):
        self.add_all(delta_time)
        if not self.show_press_enter and self.press_enter_clock.check(2):
            self.show_press_enter = True

    def on_draw(self):
        for label in self.labels:
            label.draw()

        if self.show_press_enter:
            self.press_enter.draw()
