import arcade

import mainmenu
from infoscreen import InfoScreen
from constants import WIDTH, HEIGHT


class GameOver(InfoScreen):
    def __init__(self):
        super().__init__(
            [
                arcade.Text(
                    "Game Over!",
                    WIDTH / 2,
                    HEIGHT / 2,
                    anchor_x="center",
                    anchor_y="bottom",
                    font_name="PressStart2P",
                    font_size=28,
                )
            ],
            arcade.Text(
                "Press ENTER to return to the main menu",
                WIDTH / 2,
                HEIGHT / 2 - 20,
                anchor_x="center",
                anchor_y="top",
                font_name="PressStart2P",
                font_size=14,
            ),
            mainmenu.MainMenu(),
        )

class YouWin(GameOver):
    def __init__(self):
        super().__init__()
        self.labels[0].text = "You win!"
