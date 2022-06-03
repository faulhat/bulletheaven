import arcade

from menus import MenuItem, MenuItems, Menu
import mainmenu
from constants import *


class PauseMenu(Menu):
    def __init__(self, stage: arcade.View):
        super().__init__()
        self.stage = stage
        self.options = MenuItems(
            [
                MenuItem(
                    "Return",
                    lambda menu: menu.go_back(),
                    start_x=350,
                    start_y=500,
                    font_size=18,
                    font_name="PressStart2P",
                ),
                MenuItem(
                    "Quit to title",
                    lambda menu: menu.window.show_view(mainmenu.MainMenu()),
                    start_x=350,
                    start_y=460,
                    font_size=18,
                    font_name="PressStart2P",
                ),
            ]
        )

    def go_back(self):
        self.stage.play_music()
        self.window.show_view(self.stage)

    def on_key_press(self, symbol: int, modifiers: int):
        if symbol == arcade.key.X:
            self.go_back()
        else:
            self.stage.keys.add(symbol)
            super().on_key_press(symbol, modifiers)

    def on_key_release(self, _symbol: int, _modifiers: int):
        self.stage.keys.discard(_symbol)
        return super().on_key_release(_symbol, _modifiers)

    def on_draw(self):
        self.stage.on_draw()
        arcade.draw_rectangle_filled(
            WIDTH / 2,
            HEIGHT / 2,
            WIDTH,
            HEIGHT,
            (50, 50, 200, 100),
        )
        super().on_draw()
