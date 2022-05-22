import math
from random import random
import arcade

from bullets import Bullet


# Forward declaration to avoid circular import
class Stage(arcade.View):
    bullets: arcade.SpriteList
    enemies: arcade.SpriteList


class BasicBullet(Bullet):
    def __init__(self, x: float, y: float, angle: float, stage: Stage):
        super().__init__(8, arcade.csscolor.RED, x, y, angle, 300, stage)
        stage.bullets.append(self)


class Enemy(arcade.SpriteCircle):
    def __init__(
        self,
        radius: int,
        color: arcade.Color,
        x: float,
        y: float,
        stage: Stage,
        init_hp: int,
    ):
        super().__init__(radius, color)
        self.set_position(x, y)
        stage.enemies.append(self)
        self.stage = stage
        self.hp = init_hp


class SeaStar(Enemy):
    def __init__(self, x: float, y: float, stage: Stage):
        super().__init__(15, arcade.csscolor.VIOLET, x, y, stage, 15)
        self.stopwatch = 0
        self.counter = 0
        self.shooting = False
        self.angle_offset = 0
        self.next_x, self.next_y = self.position
        self.rand_next()

    def rand_next(self):
        self.angle_offset = random() * math.pi * 2
        self.prev_x, self.prev_y = self.next_x, self.next_y
        self.next_x = random() * self.stage.window.width
        self.next_y = (random() * 1 / 2 + 1 / 2) * self.stage.window.height

    def on_update(self, delta_time: float):
        self.stopwatch += delta_time
        if not self.shooting:
            if self.stopwatch > 1:
                self.stopwatch = 0
                self.counter = 0
                self.shooting = True
            else:
                x = self.prev_x + (self.next_x - self.prev_x) * self.stopwatch
                y = self.prev_y + (self.next_y - self.prev_y) * self.stopwatch
                self.set_position(x, y)
        else:
            if self.stopwatch > 1 / 4:
                self.stopwatch = 0
                self.counter += 1
                if self.counter == 4:
                    self.shooting = False
                    self.rand_next()
                else:
                    for i in range(4):
                        angle = self.angle_offset + math.pi * 2 / 4 * i
                        x = self.position[0] + math.cos(angle) * 2
                        y = self.position[1] + math.sin(angle) * 2
                        BasicBullet(x, y, angle, self.stage)

                    self.angle_offset += math.pi * 2 / 50


class DualWielder(Enemy):
    SPEED = 300

    angle: float

    def __init__(self, x: float, stage: Stage):
        super().__init__(
            15, arcade.csscolor.INDIGO, x, stage.window.height + 10, stage, 10
        )
        self.target_x = stage.window.width - x
        self.target_y = -10
        self.stopwatch = 0
        self.switch = 0

        if self.target_x - x == 0:
            # Avoid division by zero.
            self.angle = math.pi * 3 / 2
        else:
            self.angle = (
                -math.atan((self.target_x - x) / -(stage.window.height + 20))
                - math.pi / 2
            )

    def on_update(self, delta_time: float):
        if self.position[1] < self.target_y:
            self.remove_from_sprite_lists()
            return

        self.stopwatch += delta_time
        if self.stopwatch > 0.35:
            self.stopwatch = 0
            if self.switch == 0:
                x = self.position[0] - 18
                BasicBullet(x, self.position[1], math.pi * 3 / 2, self.stage)
                self.switch = 1
            else:
                x = self.position[0] + 18
                BasicBullet(x, self.position[1], math.pi * 3 / 2, self.stage)
                self.switch = 0

        x = self.position[0] + math.cos(self.angle) * DualWielder.SPEED * delta_time
        y = self.position[1] + math.sin(self.angle) * DualWielder.SPEED * delta_time
        self.set_position(x, y)
