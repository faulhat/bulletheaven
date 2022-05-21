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

    def setup(self):
        self.show_view(mainmenu.MainMenu())

    def on_update(self, delta_time: float):
        super().on_update(delta_time)

        self.counter += delta_time
        if self.counter > 1.0:
            self.fps = self.n_frames
            self.n_frames = 0
            self.counter = 0
        else:
            self.n_frames += 1

    def on_draw(self):
        self.clear()
        self.current_view.on_draw()
        arcade.draw_text(f"FPS: {self.fps}", 10, 10, font_size=20)
        self.flip()

def run_game() -> None:
    window = Game()
    window.setup()
    arcade.run()
