import os
import arcade

from stopwatch import GameObject
from menus import MenuItem, MenuItems, Menu
from levelselect import LevelSelect
from instructions import Instructions
from constants import *


class MainMenu(Menu, GameObject):
    # Directory containing animation frames
    TITLE_FRAMES_DIR = os.path.join("assets", "title")

    # Frames of animation that the title screen cycles through
    TITLE_FRAME_FILES = [
        "title.png",
        "title1.png",
        "title2.png",
    ]

    # Seconds between frames
    INTERVAL = 0.5

    def __init__(self):
        Menu.__init__(self)
        GameObject.__init__(self)

        self.animation_clock = self.new_stopwatch()
        self.frame = 0
        self.title_frames = [
            arcade.load_texture(os.path.join(MainMenu.TITLE_FRAMES_DIR, frame_file))
            for frame_file in MainMenu.TITLE_FRAME_FILES
        ]

        self.options = MenuItems(
            [
                MenuItem(
                    "Start!",
                    lambda view: view.window.show_view(Instructions()),
                    start_x=300,
                    start_y=280,
                    font_size=18,
                    font_name="PressStart2P",
                ),
                MenuItem(
                    "Select stage...",
                    lambda view: view.window.show_view(LevelSelect()),
                    start_x=300,
                    start_y=240,
                    font_size=18,
                    font_name="PressStart2P",
                ),
                MenuItem(
                    "Quit.",
                    lambda _: arcade.exit(),
                    start_x=300,
                    start_y=200,
                    font_size=18,
                    font_name="PressStart2P",
                ),
            ]
        )

        self.copylabel = arcade.Text(
            "(C) Thomas Faulhaber, 2022", 10, 30, font_size=14, font_name="PressStart2P"
        )

    def on_update(self, delta_time: float):
        self.animation_clock.add(delta_time)
        if self.animation_clock.check_reset(MainMenu.INTERVAL):
            self.frame = (self.frame + 1) % len(self.title_frames)

    def on_draw(self):
        arcade.draw_texture_rectangle(
            WIDTH // 2,
            HEIGHT // 2,
            WIDTH,
            HEIGHT,
            self.title_frames[self.frame],
        )

        super().on_draw()

        arcade.draw_rectangle_filled(
            500, 350, 510, 10 * (1 + 5**0.5) / 2, arcade.csscolor.WHITE
        )
        arcade.draw_rectangle_filled(
            500, 150, 510, 10 * (1 + 5**0.5) / 2, arcade.csscolor.WHITE
        )
        arcade.draw_rectangle_filled(250, 250, 10, 200, arcade.csscolor.WHITE)
        arcade.draw_rectangle_filled(750, 250, 10, 200, arcade.csscolor.WHITE)

        self.copylabel.draw()
