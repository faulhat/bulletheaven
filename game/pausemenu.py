import arcade

from menus import MenuItem, MenuItems, Menu
import mainmenu


class PauseMenu(Menu):
    def __init__(self, stage: arcade.View):
        super().__init__()
        self.stage = stage
        self.options = MenuItems(
            [
                MenuItem(
                    "Return",
                    lambda _: self.window.show_view(self.stage),
                    start_x=350,
                    start_y=500,
                    font_size=18,
                    font_name="PressStart2P",
                ),
                MenuItem(
                    "Quit to title",
                    lambda _: self.window.show_view(mainmenu.MainMenu()),
                    start_x=350,
                    start_y=460,
                    font_size=18,
                    font_name="PressStart2P",
                ),
            ]
        )

    def on_key_press(self, symbol: int, modifiers: int):
        if symbol == arcade.key.X:
            self.window.show_view(self.stage)
            return

        self.stage.on_key_press(symbol, modifiers)
        return super().on_key_press(symbol, modifiers)

    def on_key_release(self, _symbol: int, _modifiers: int):
        self.stage.on_key_release(_symbol, _modifiers)
        return super().on_key_release(_symbol, _modifiers)

    def on_draw(self):
        self.stage.on_draw()
        arcade.draw_rectangle_filled(
            self.window.width / 2,
            self.window.height / 2,
            self.window.width,
            self.window.height,
            (100, 100, 100, 100),
        )
        super().on_draw()
