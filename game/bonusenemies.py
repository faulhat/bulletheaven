import math
from random import random
import arcade

from stage import Stage
from enemy import Enemy, Boss, DartingEnemy
from l1enemies import BasicBullet
from constants import *


class BouncingBullet(BasicBullet):
    def __init__(
        self, x: float, y: float, angle: float, stage: Stage, n_bounces: int = 1
    ):
        super().__init__(x, y, angle, stage)
        self.n_bounces = n_bounces
        self.color = arcade.csscolor.YELLOW
        self.speed = 200

    def on_update(self, delta_time: float):
        if self.n_bounces:
            x, y = self.position
            next_x = x + math.cos(self.angle) * delta_time * self.speed
            next_y = y + math.sin(self.angle) * delta_time * self.speed

            if next_x > WIDTH - self.RADIUS or next_x < self.RADIUS:
                self.n_bounces -= 1
                next_x = max(self.RADIUS, min(WIDTH - self.RADIUS, next_x))
                next_y = y + (next_x - x) / math.cos(self.angle)
                self.angle = -self.angle + math.pi
            elif next_y > HEIGHT - self.RADIUS or next_y < self.RADIUS:
                self.n_bounces -= 1
                next_y = max(self.RADIUS, min(HEIGHT - self.RADIUS, next_y))
                next_x = x + (next_y - y) / math.sin(self.angle)
                self.angle = -self.angle

            if not self.n_bounces:
                self.color = arcade.csscolor.VIOLET
                self.speed = 300

            self.set_position(next_x, next_y)
        else:
            super().on_update(delta_time)


class Gatling(DartingEnemy, Boss):
    BOSS_INIT_HP = 40
    COLOR = arcade.csscolor.GAINSBORO
    NAME = "Gatling"

    def __init__(
        self,
        x: float,
        y: float,
        stage: Stage,
        n_directions: int = 6,
        n_rounds: int = 6,
        interval: float = 2,
    ):
        DartingEnemy.__init__(
            self, x, y, stage, Gatling.BOSS_INIT_HP, interval=interval
        )
        Boss.__init__(self)

        self.fire_clock = self.new_stopwatch()
        self.n_directions = n_directions
        self.n_rounds = n_rounds
        self.round = 0

    def change_state(self):
        super().change_state()
        self.fire_clock.reset()
        self.round = 0

    def on_update(self, delta_time: float):
        super().on_update(delta_time)

        if not self.shooting:
            if self.dart_clock.check(self.interval):
                self.change_state()
            else:
                self.dart_update()
        elif self.fire_clock.check_reset(self.interval / self.n_rounds):
            x, y = self.position
            angle = random() * math.pi * 2
            for i in range(self.n_directions):
                BouncingBullet(
                    x + math.cos(angle) * self.RADIUS,
                    y + math.sin(angle) * self.RADIUS,
                    angle,
                    self.stage,
                )
                angle += math.pi * 2 / self.n_directions

            self.round += 1
            if self.round == self.n_rounds:
                self.change_state()
