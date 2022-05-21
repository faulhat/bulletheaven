import arcade

import mainmenu


WIN_WIDTH = 1000
WIN_HEIGHT = 800
WIN_TITLE = "Bullet Heaven!"


class Game(arcade.Window):
    def __init__(self):
        super().__init__(WIN_WIDTH, WIN_HEIGHT, WIN_TITLE, center_window=True)
        arcade.set_background_color(arcade.csscolor.BLACK)

        self.fps = 0
        self.counter = 0
        self.n_frames = 0
        self.fps_label = arcade.Text(f"FPS:   ", 900, 30, font_size=14, font_name="PressStart2P", anchor_x="right")
        self.copylabel = arcade.Text("(C) Thomas Faulhaber, 2022", 10, 30, font_size=14, font_name="PressStart2P")

    def setup(self):
        self.show_view(mainmenu.MainMenu())

    def on_update(self, delta_time: float):
        super().on_update(delta_time)

        self.counter += delta_time
        if self.counter > 1.0:
            self.fps = self.n_frames
            self.n_frames = 0
            self.counter = 0

            self.fps_label.text = f"FPS: {self.fps}"
        else:
            self.n_frames += 1

    def on_draw(self):
        self.clear()
        self.current_view.on_draw()
        self.fps_label.draw()
        self.copylabel.draw()

def run_game():
    window = Game()
    window.setup()
    arcade.run()
