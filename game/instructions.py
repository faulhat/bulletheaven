import arcade

from infoscreen import InfoScreen
from stages import *


class Instructions(InfoScreen):
    INSTRUCTIONS = [
        "INSTRUCTIONS",
        "Use the arrow keys or WASD to move",
        "Use X to pause",
        "Hold Z to slow down",
        "Avoid the bullets (hollow)",
        "Shoot the enemies (solid)",
        "When you kill an enemy you score a point",
        "5 points = 1 HP",
        "Grab the charms (square)",
        "Press Q to use a charm and enter SERENITY MODE.",
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
            L1Stage1(),
        )
