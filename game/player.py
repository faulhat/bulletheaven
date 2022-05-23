import math
import arcade

from bullets import Bullet
from constants import *


class Player(arcade.SpriteCircle):
    SPEED = 400

    class FriendlyBullet(Bullet):
        def __init__(self, x: float, y: float, stage: arcade.View):
            super().__init__(
                8, (65, 105, 255, 240), x, y, math.pi * 1 / 2, 600, stage, friendly=True
            )

    def __init__(self, init_x: float, init_y: float, stage: arcade.View):
        super().__init__(12, arcade.csscolor.ALICE_BLUE)
        self.stage = stage
        self.set_position(init_x, init_y)

        self.hp = 10
        self.score = 0
        self.invincible = False
        self.hp_label = arcade.Text(
            f"HP: {self.hp}",
            stage.window.width - 30,
            stage.window.height - 70,
            anchor_x="right",
            font_name="PressStart2P",
            font_size=18,
        )

        self.score_label = arcade.Text(
            f"SCORE: {self.score}",
            30,
            stage.window.height - 70,
            font_name="PressStart2P",
            font_size=18,
        )

        self.dead = False
        self.slow = False
        self.firing_stopwatch = 0

    def set_hp(self, hp: int):
        self.hp = hp
        self.hp_label.text = f"HP: {hp}"
    
    def inc_score(self, n: int = 1):
        self.score += n
        self.score_label.text = f"SCORE: {self.score}"

        if self.score % 5 == 0:
            self.set_hp(self.hp + 1)

    def set_position(self, x: float, y: float):
        x = min(
            WIDTH - self.width / 2,
            max(self.width / 2, x),
        )
        y = min(
            self.stage.window.height - self.width / 2,
            max(self.width / 2, y),
        )
        super().set_position(x, y)
