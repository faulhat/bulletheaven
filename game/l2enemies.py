import math
from random import random
import arcade

from bullets import Bullet
from l1enemies import Enemy, DartingEnemy
from stage import Stage
from constants import *


def distance(x1: float, y1: float, x2: float, y2: float) -> float:
    return math.sqrt(math.pow(x1 - x2, 2) + math.pow(y1 - y2, 2))


class RadialBullet(Bullet):
    RADIUS = 8
    STATE_CIRCLE_FORMATION = 0
    STATE_FREEZE = 1
    STATE_FIRE = 2
    SPEED = 300

    def __init__(self, shooter: Enemy, angle: float, go_distance: float):
        self.origin_x = shooter.position[0] + math.cos(angle) * shooter.width / 2
        self.origin_y = shooter.position[1] + math.sin(angle) * shooter.width / 2
        super().__init__(
            RadialBullet.RADIUS,
            arcade.csscolor.VIOLET,
            self.origin_x,
            self.origin_y,
            angle,
            RadialBullet.SPEED,
            shooter.stage,
        )
        self.state = RadialBullet.STATE_CIRCLE_FORMATION
        self.go_distance = go_distance

    def go_fire(self, target_x: float, target_y: float):
        self.state = RadialBullet.STATE_FIRE
        x, y = self.position
        if y - target_y == 0:
            if target_x > x:
                self.angle = 0
            else:
                self.angle = math.pi
        else:
            self.angle = math.atan2(target_y - y, target_x - x)

    def on_update(self, delta_time: float):
        if self.state == RadialBullet.STATE_CIRCLE_FORMATION:
            x, y = self.position
            change_x, change_y = 0, 0
            if distance(x, y, self.origin_x, self.origin_y) < self.go_distance:
                change_x = math.cos(self.angle) * delta_time * self.speed
                change_y = math.sin(self.angle) * delta_time * self.speed
            else:
                self.state = RadialBullet.STATE_FREEZE
            
            self.set_position(x + change_x, y + change_y)
            if self.out_of_bounds():
                self.set_position(x, y)
                self.state = RadialBullet.STATE_FREEZE
        elif self.state == RadialBullet.STATE_FIRE:
            super().on_update(delta_time)


class CircleFire(DartingEnemy):
    RADIUS = 15
    INIT_HP = 20

    def __init__(
        self,
        x: float,
        y: float,
        stage: Stage,
        n_bullets: int = 15,
        interval: float = 0.7,
        fire_radius: float = 100,
    ):
        super().__init__(
            CircleFire.RADIUS, x, y, stage, CircleFire.INIT_HP, interval=interval
        )
        self.n_bullets = n_bullets
        self.counter = 0
        self.bullets_active = arcade.SpriteList()
        self.shooting = False
        self.angle = 0
        self.fire_radius = fire_radius

    def on_update(self, delta_time: float):
        super().on_update(delta_time)

        if not self.shooting:
            if self.stopwatch > self.interval:
                self.stopwatch = 0
                self.shooting = True
            else:
                self.dart_update()
        else:
            if self.stopwatch > self.interval / self.n_bullets:
                self.stopwatch = 0
                self.counter += 1
                if self.counter > self.n_bullets:
                    all_bullets_out = True
                    for bullet in self.bullets_active:
                        if bullet.state != RadialBullet.STATE_FREEZE:
                            all_bullets_out = False

                    if all_bullets_out:
                        for bullet in self.bullets_active:
                            bullet.go_fire(*self.stage.player.position)
                        
                        self.bullets_active.clear()
                        self.shooting = False
                        self.counter = 0
                        self.rand_next()
                else:
                    self.angle += math.pi * 2 / self.n_bullets
                    self.bullets_active.append(
                        RadialBullet(self, self.angle, self.fire_radius)
                    )
