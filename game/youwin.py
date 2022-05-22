import arcade

import gameover

class YouWin(gameover.GameOver):
    def __init__(self):
        super().__init__()
        self.gameover.text = "You win!"
