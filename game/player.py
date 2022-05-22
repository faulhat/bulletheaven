import math
import arcade

from bullets import Bullet


class Player(arcade.SpriteCircle):
    class FriendlyBullet(Bullet):
        def __init__(self, x: float, y: float, stage: arcade.View):
            super().__init__(
                6, (65, 105, 255, 240), x, y, math.pi * 1 / 2, 600, stage, friendly=True
            )

    def __init__(
        self, init_x: float, init_y: float, hp_label_x: float, hp_label_y: float
    ):
        super().__init__(15, arcade.csscolor.ALICE_BLUE)
        self.hp = 5
        self.invincible = False
        self.speed = 500
        self.set_position(init_x, init_y)
        self.hp_label = arcade.Text(
            "HP: 5",
            hp_label_x,
            hp_label_y,
            anchor_x="right",
            font_name="PressStart2P",
            font_size=18,
        )
        self.dead = False
        self.slow = False
        self.firing_stopwatch = 0

    def set_hp(self, hp: int):
        self.hp = hp
        self.hp_label.text = f"HP: {hp}"
