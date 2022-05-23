import arcade

from infoscreen import InfoScreen
from stages import L1Stage1


class Instructions(InfoScreen):
    INSTRUCTIONS = [
        "INSTRUCTIONS",
        "Use the arrow keys to move",
        "Use X to pause",
        "Hold S to slow down",
        "Avoid the bullets (red)",
        "Try to hit the enemies (pink)",
        "When you kill an enemy you score a point",
        "5 points = 1 HP",
    ]

    def __init__(self):
        super().__init__(
            [
                arcade.Text(
                    instruction,
                    500,
                    700 - i * 50,
                    font_size=14,
                    font_name="PressStart2P",
                    anchor_x="center",
                )
                for i, instruction in enumerate(Instructions.INSTRUCTIONS)
            ],
            arcade.Text(
                "Press ENTER to continue",
                500,
                200,
                font_size=14,
                font_name="PressStart2P",
                anchor_x="center",
            ),
            L1Stage1()
        )
