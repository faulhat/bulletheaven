import math
import os
from typing import Callable
import arcade


class MenuItem:
    def __init__(self, text: str, does: Callable[[arcade.View], None], *args, **kwargs):
        self.text = text
        self.label = arcade.Text(f" {self.text}", *args, **kwargs)
        self.selected = False
        self.does = does
    
    def select(self):
        if not self.selected:
            self.label.text = f"> {self.text}"
            self.selected = True
    
    def deselect(self):
        if self.selected:
            self.label.text = f" {self.text}"
            self.selected = False


class MenuItems:
    def __init__(self, items: list[MenuItem], selected: int = 0):
        self.items = items
        self.selected = selected
        for i, item in enumerate(self.items):
            if i == self.selected:
                item.select()
            else:
                item.deselect()

    def select(self, i: int):
        self.items[self.selected].deselect()
        self.selected = i
        self.items[self.selected].select()
    
    def decrement(self):
        if self.selected > 0:
            self.select(self.selected - 1)

    def increment(self):
        if self.selected < len(self.items) - 1:
            self.select(self.selected + 1)
    
    def get(self) -> MenuItem:
        return self.items[self.selected]


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
    INTERVAL = .5

    # Menu options
    OPTIONS = [
        "Start!",
        "Quit.",
    ]

    def __init__(self):
        super().__init__()
        self.counter = 0
        self.frame = 0
        self.title_frames = [arcade.load_texture(os.path.join(MainMenu.TITLE_FRAMES_DIR, frame_file)) for frame_file in MainMenu.TITLE_FRAME_FILES]

        self.options = MenuItems([
            MenuItem(
                "Start!",
                lambda _: None,
                start_x=200, start_y=280,
                font_size=18, font_name="PressStart2P",
            ),
            MenuItem(
                "Quit.",
                lambda _: arcade.exit(),
                start_x=200, start_y=240,
                font_size=18, font_name="PressStart2P",
            ),
        ])
    
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
            self.window.width // 2, self.window.height // 2,
            self.window.width, self.window.height,
            self.title_frames[self.frame],
        )

        for option in self.options.items:
            option.label.draw()

        arcade.draw_rectangle_filled(400, 350, 710, 10 * (1 + 5 ** 0.5) / 2, arcade.csscolor.WHITE)
        arcade.draw_rectangle_filled(400, 150, 710, 10 * (1 + 5 ** 0.5) / 2, arcade.csscolor.WHITE)
        arcade.draw_rectangle_filled(50, 250, 10, 200, arcade.csscolor.WHITE)
        arcade.draw_rectangle_filled(750, 250, 10, 200, arcade.csscolor.WHITE)
        