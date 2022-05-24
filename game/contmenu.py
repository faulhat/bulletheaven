import arcade

from player import Player
from menus import MenuItem, MenuItems, Menu
import mainmenu
from constants import *


class Stage(arcade.View):
    player: Player


class ContinueMenu(Menu):
    def __init__(self, stage: Stage):
        super().__init__()
        self.stage = stage
        self.options = MenuItems(
            [
                MenuItem(
                    "Continue",
                    lambda menu: menu.use_continue(),
                    start_x=150,
                    start_y=500,
                    font_size=18,
                    font_name="PressStart2P",
                ),
                MenuItem(
                    "Give up",
                    lambda menu: menu.window.show_view(mainmenu.MainMenu()),
                    start_x=150,
                    start_y=460,
                    font_size=18,
                    font_name="PressStart2P",
                ),
            ]
        )

        continue_text: str
        if stage.player.n_continues == 1:
            continue_text = f"You have 1 continue remaining."
        else:
            continue_text = f"You have {stage.player.n_continues} continues remaining."

        self.continue_label = arcade.Text(
            continue_text,
            start_x=150,
            start_y=540,
            font_size=18,
            font_name="PressStart2P",
        )

    def use_continue(self):
        self.stage.player.invincible = True
        self.stage.player.set_hp(Player.INIT_HP)
        self.stage.player.n_continues -= 1
        self.window.show_view(self.stage)

    def on_key_press(self, symbol: int, modifiers: int):
        self.stage.on_key_press(symbol, modifiers)
        return super().on_key_press(symbol, modifiers)

    def on_key_release(self, _symbol: int, _modifiers: int):
        self.stage.on_key_release(_symbol, _modifiers)
        return super().on_key_release(_symbol, _modifiers)

    def on_draw(self):
        self.stage.on_draw()
        arcade.draw_rectangle_filled(
            WIDTH / 2,
            HEIGHT / 2,
            WIDTH,
            HEIGHT,
            (200, 50, 50, 100),
        )
        self.continue_label.draw()
        super().on_draw()
