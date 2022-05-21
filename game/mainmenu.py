import os
import arcade

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

    def __init__(self):
        super().__init__()
        self.counter = 0
        self.frame = 0
        self.title_frames = [arcade.load_texture(os.path.join(MainMenu.TITLE_FRAMES_DIR, frame_file)) for frame_file in MainMenu.TITLE_FRAME_FILES]

    
    def on_update(self, delta_time: float) -> None:
        self.counter += delta_time
        if self.counter >= MainMenu.INTERVAL:
            self.counter = 0
            self.frame = (self.frame + 1) % len(self.title_frames)
    
    def on_draw(self) -> None:
        arcade.draw_texture_rectangle(
            self.window.width // 2, self.window.height // 2,
            self.window.width, self.window.height,
            self.title_frames[self.frame],
        )
        