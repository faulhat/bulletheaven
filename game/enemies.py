import math
from random import random
import arcade

from bullets import Bullet
from stage import Stage


class SimpleEnemy(arcade.SpriteCircle):
    class SEBullet(Bullet):
        def __init__(self, x, y, angle):
            super().__init__(8, arcade.csscolor.RED, x, y, angle, 300)

    def __init__(self, x: float, y: float, stage: Stage):
        super().__init__(15, arcade.csscolor.ORANGE_RED)
        self.set_position(x, y)
        self.stage = stage
        self.stopwatch = 0
        self.counter = 0
        self.shooting = False
        self.angle_offset = 0
        self.next_x, self.next_y = self.position
        self.rand_next()
        self.hp = 15

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
            if self.stopwatch > 1 / 8:
                self.stopwatch = 0
                self.counter += 1
                if self.counter == 8:
                    self.shooting = False
                    self.rand_next()
                else:
                    for i in range(5):
                        angle = self.angle_offset + math.pi * 2 / 5 * i
                        x = self.position[0] + math.cos(angle) * 2
                        y = self.position[1] + math.sin(angle) * 2
                        self.stage.bullets.append(SimpleEnemy.SEBullet(x, y, angle))

                    self.angle_offset += math.pi * 2 / 60
