import math
import arcade

from enemy import Enemy, Boss
from l1enemies import BasicBullet
from stage import Stage
from constants import *


class AimingTurret(Enemy):
    RADIUS = 15
    INIT_HP = 9
    COLOR = arcade.csscolor.AQUAMARINE
    SPEED = 300

    def __init__(self, y: float, stage: Stage, direction: int, n_bullets: int = 4):
        x: float
        if direction == LEFT:
            x = WIDTH + AimingTurret.RADIUS
        elif direction == RIGHT:
            x = -AimingTurret.RADIUS

        super().__init__(AimingTurret.RADIUS, x, y, stage, AimingTurret.INIT_HP)
        self.fire_watch = 0
        self.counter = 0
        self.shooting = False
        self.n_bullets = n_bullets
        self.direction = direction
    
    def on_update(self, delta_time: float):
        super().on_update(delta_time)
        self.fire_watch += delta_time

        x, y = self.position
        if self.shooting:
            if self.fire_watch > 0.2:
                self.fire_watch = 0
                self.counter += 1

                player_x, player_y = self.stage.player.position
                angle = math.atan2(player_y - y, player_x - x)
                BasicBullet(x, y + AimingTurret.RADIUS, angle, self.stage)

                if self.counter > self.n_bullets:
                    self.counter = 0
                    self.shooting = False
        else:
            if self.fire_watch > 0.5:
                self.fire_watch = 0
                self.shooting = True

        if self.direction == LEFT:
            x -= AimingTurret.SPEED * delta_time
            if x < -AimingTurret.RADIUS:
                self.on_die()
        elif self.direction == RIGHT:
            x += AimingTurret.SPEED * delta_time
            if x > WIDTH + AimingTurret.RADIUS:
                self.on_die()
        
        self.set_position(x, y)
