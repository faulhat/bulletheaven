import math
import arcade

from bullets import Bullet


class Player(arcade.SpriteCircle):
    class FriendlyBullet(Bullet):
        def __init__(self, x: float, y: float, stage: arcade.View):
            super().__init__(
                6, (65, 105, 255, 240), x, y, math.pi * 1 / 2, 600, stage, friendly=True
            )

    def __init__(self, init_x: float, init_y: float, stage: arcade.View):
        super().__init__(15, arcade.csscolor.ALICE_BLUE)
        self.stage = stage
        self.set_position(init_x, init_y)

        self.hp = 5
        self.invincible = False
        self.speed = 500
        self.hp_label = arcade.Text(
            "HP: 5",
            stage.window.width - 30,
            stage.window.height - 30,
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

    def set_position(self, x: float, y: float):
        x = min(
            self.stage.window.width - self.width / 2,
            max(self.width / 2, x),
        )
        y = min(
            self.stage.window.height - self.width / 2,
            max(self.width / 2, y),
        )
        super().set_position(x, y)
