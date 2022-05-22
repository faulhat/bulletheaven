import os
import arcade

from menus import MenuItem, MenuItems
from stage import Stage

class MainMenu(arcade.View):
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
        super().__init__()
        self.counter = 0
        self.frame = 0
        self.title_frames = [
            arcade.load_texture(os.path.join(MainMenu.TITLE_FRAMES_DIR, frame_file))
            for frame_file in MainMenu.TITLE_FRAME_FILES
        ]

        self.options = MenuItems(
            [
                MenuItem(
                    "Start!",
                    lambda _: self.window.show_view(Stage()),
                    start_x=350,
                    start_y=280,
                    font_size=18,
                    font_name="PressStart2P",
                ),
                MenuItem(
                    "Quit.",
                    lambda _: arcade.exit(),
                    start_x=350,
                    start_y=240,
                    font_size=18,
                    font_name="PressStart2P",
                ),
            ]
        )

        self.copylabel = arcade.Text(
            "(C) Thomas Faulhaber, 2022", 10, 30, font_size=14, font_name="PressStart2P"
        )

    def on_key_press(self, symbol: int, modifiers: int):
        if symbol == arcade.key.UP:
            self.options.decrement()

        if symbol == arcade.key.DOWN:
            self.options.increment()

        if symbol == arcade.key.ENTER:
            self.options.get().does(self)

        return super().on_key_press(symbol, modifiers)

    def on_update(self, delta_time: float):
        self.counter += delta_time
        if self.counter >= MainMenu.INTERVAL:
            self.counter = 0
            self.frame = (self.frame + 1) % len(self.title_frames)

    def on_draw(self):
        arcade.draw_texture_rectangle(
            self.window.width // 2,
            self.window.height // 2,
            self.window.width,
            self.window.height,
            self.title_frames[self.frame],
        )

        for option in self.options.items:
            option.label.draw()

        arcade.draw_rectangle_filled(
            500, 350, 510, 10 * (1 + 5**0.5) / 2, arcade.csscolor.WHITE
        )
        arcade.draw_rectangle_filled(
            500, 150, 510, 10 * (1 + 5**0.5) / 2, arcade.csscolor.WHITE
        )
        arcade.draw_rectangle_filled(250, 250, 10, 200, arcade.csscolor.WHITE)
        arcade.draw_rectangle_filled(750, 250, 10, 200, arcade.csscolor.WHITE)

        self.copylabel.draw()
