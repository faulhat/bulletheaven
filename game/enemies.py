import math
from random import random
import arcade

from bullets import Bullet
from stage import Stage
from constants import *


class BasicBullet(Bullet):
    def __init__(self, x: float, y: float, angle: float, stage: Stage):
        super().__init__(8, arcade.csscolor.RED, x, y, angle, 400, stage)


class Enemy(arcade.SpriteCircle):
    def __init__(
        self,
        radius: int,
        x: float,
        y: float,
        stage: Stage,
        init_hp: int,
    ):
        super().__init__(radius, arcade.csscolor.VIOLET)
        self.set_position(x, y)
        stage.enemies.append(self)
        self.stage = stage
        self.hp = init_hp


class SeaStar(Enemy):
    RADIUS = 15

    def __init__(
        self,
        x: float,
        y: float,
        stage: Stage,
        n_spines: int = 5,
        interval: float = 1,
        n_bullets: int = 6,
        double: bool = False,
    ):
        super().__init__(SeaStar.RADIUS, x, y, stage, 10)
        self.stopwatch = 0
        self.counter = 0
        self.shooting = False
        self.angle_offset = 0
        self.next_x, self.next_y = self.position
        self.rand_next()
        self.n_spines = n_spines
        self.interval = interval
        self.n_bullets = n_bullets
        self.double = double

    def rand_next(self):
        self.angle_offset = random() * math.pi * 2
        self.prev_x, self.prev_y = self.next_x, self.next_y
        self.next_x = (
            random() * (WIDTH - 2 * self.width / 2) + self.width / 2
        )
        self.next_y = (random() * 1 / 2 + 1 / 2) * (
            self.stage.window.height - 2 * self.width / 2
        )

    def on_update(self, delta_time: float):
        self.stopwatch += delta_time
        if not self.shooting:
            if self.stopwatch > self.interval:
                self.stopwatch = 0
                self.counter = 0
                self.shooting = True
            else:
                x = (
                    self.prev_x
                    + (self.next_x - self.prev_x) * self.stopwatch / self.interval
                )
                y = (
                    self.prev_y
                    + (self.next_y - self.prev_y) * self.stopwatch / self.interval
                )
                self.set_position(x, y)
        else:
            if self.stopwatch > self.interval / self.n_bullets:
                self.stopwatch = 0
                self.counter += 1
                if (not self.double and self.counter > self.n_bullets) or (
                    self.double and self.counter > self.n_bullets * 2
                ):
                    self.shooting = False
                    self.rand_next()
                else:
                    for i in range(self.n_spines):
                        angle = self.angle_offset + math.pi * 2 / self.n_spines * i
                        x = self.position[0] + math.cos(angle) * 2
                        y = self.position[1] + math.sin(angle) * 2
                        BasicBullet(x, y, angle, self.stage)

                    if self.counter <= self.n_bullets:
                        self.angle_offset += math.pi * 2 / 50
                    else:
                        self.angle_offset -= math.pi * 2 / 50


class FallingStar(Enemy):
    SPEED = 300

    angle: float

    def __init__(self, x: float, stage: Stage):
        super().__init__(
            15, x, stage.window.height + 10, stage, 10
        )
        self.target_x = stage.window.width - x
        self.target_y = -10
        self.stopwatch = 0

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
        if self.stopwatch > 0.5:
            self.stopwatch = 0
            opp_angle = -self.angle + math.pi
            x = self.position[0] + math.cos(opp_angle)
            BasicBullet(x, self.position[1], opp_angle, self.stage)

        x = self.position[0] + math.cos(self.angle) * FallingStar.SPEED * delta_time
        y = self.position[1] + math.sin(self.angle) * FallingStar.SPEED * delta_time
        self.set_position(x, y)


class Turret(Enemy):
    LEFT = -1
    RIGHT = 1
    RADIUS = 12

    def __init__(
        self,
        y: float,
        direction: int,
        speed: float,
        rotation_speed: float,
        arms: int,
        stage: Stage,
    ):
        super().__init__(12, 0, y, stage, 10)
        x: float
        if direction == Turret.LEFT:
            x = WIDTH + Turret.RADIUS
        elif direction == Turret.RIGHT:
            x = -Turret.RADIUS

        self.set_position(x, y)
        self.speed = speed
        self.rotation_speed = rotation_speed

        # Direction should be -1 for left and 1 for right
        self.direction = direction
        self.arms = arms
        self.angle = 0
        self.stopwatch = 0

    def on_update(self, delta_time: float):
        x = self.position[0]
        y = self.position[1]
        if (self.direction > 0 and x > WIDTH + self.width / 2) or (
            self.direction < 0 and x < -self.width / 2
        ):
            self.remove_from_sprite_lists()
            return
        else:
            x += self.speed * delta_time * self.direction
            self.set_position(x, y)
            self.angle += delta_time * self.rotation_speed

        self.stopwatch += delta_time
        if self.stopwatch > 0.25:
            self.stopwatch = 0
            for i in range(self.arms):
                angle = self.angle + i * 2 * math.pi / self.arms
                BasicBullet(
                    x + math.cos(angle) * self.width / 2,
                    y + math.sin(angle) * self.width / 2,
                    angle,
                    self.stage,
                )
