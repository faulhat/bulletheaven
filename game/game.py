import arcade

from stopwatch import GameObject
import mainmenu
from constants import *

WIN_TITLE = "Bullet Heaven!"


class Game(arcade.Window, GameObject):
    def __init__(self):
        arcade.Window.__init__(self, WIDTH, HEIGHT, WIN_TITLE, center_window=True)
        GameObject.__init__(self)
        arcade.set_background_color(arcade.csscolor.BLACK)

        self.fps = 0
        self.fps_clock = self.new_stopwatch()
        self.n_frames = 0
        self.fps_label = arcade.Text(
            f"FPS:   ",
            900,
            30,
            font_size=14,
            font_name="PressStart2P",
            anchor_x="right",
        )

    def setup(self):
        self.show_view(mainmenu.MainMenu())

    def on_update(self, delta_time: float):
        super().on_update(delta_time)
        self.add_all(delta_time)

        self.n_frames += 1
        if self.fps_clock.check_reset(1):
            self.fps = self.n_frames
            self.n_frames = 0
            self.fps_label.text = f"FPS: {self.fps}"

    def on_draw(self):
        self.clear()
        self.current_view.on_draw()
        self.fps_label.draw()


def run_game():
    window = Game()
    window.setup()
    arcade.run()
