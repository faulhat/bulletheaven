import math
import arcade

from bullets import Bullet
from constants import *


class FriendlyBullet(Bullet):
    def __init__(self, x: float, y: float, stage: arcade.View):
        super().__init__(
            8, arcade.csscolor.BLUE, x, y, math.pi * 1 / 2, 600, stage, friendly=True
        )
        

class Player(arcade.SpriteCircle):
    RADIUS = 15
    SPEED = 400
    INIT_HP = 10

    def __init__(self, init_x: float, init_y: float, stage: arcade.View):
        super().__init__(Player.RADIUS, arcade.csscolor.WHITE)
        self.normal_texture = self.texture
        self.on_hit_texture = arcade.make_circle_texture(
            Player.RADIUS * 2, arcade.csscolor.RED
        )

        self.stage = stage
        self.set_position(init_x, init_y)

        self.hp = Player.INIT_HP
        self.score = 0
        self.invincible = False
        self.hp_label = arcade.Text(
            f"HP: {self.hp}",
            WIDTH - 30,
            HEIGHT - 70,
            anchor_x="right",
            font_name="PressStart2P",
            font_size=18,
        )

        self.score_label = arcade.Text(
            f"SCORE: {self.score}",
            30,
            HEIGHT - 70,
            font_name="PressStart2P",
            font_size=18,
        )

        self.dead = False
        self.slow = False
        self.firing_stopwatch = 0
        self.blink = False

        self.n_continues = 2

    def set_score(self, score: int):
        self.score = score
        self.score_label.text = f"SCORE: {self.score}"

    def set_hp(self, hp: int):
        self.hp = hp
        self.hp_label.text = f"HP: {hp}"

    def inc_score(self, n: int = 1):
        for _ in range(n):
            self.score += 1
            if self.score % 5 == 0:
                self.set_hp(self.hp + 1)
            
        self.score_label.text = f"SCORE: {self.score}"

    def set_position(self, x: float, y: float):
        x = min(
            WIDTH - self.width / 2,
            max(self.width / 2, x),
        )
        y = min(
            HEIGHT - self.width / 2,
            max(self.width / 2, y),
        )
        super().set_position(x, y)
