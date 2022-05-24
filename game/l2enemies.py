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
    RADIUS = 4
    STATE_CIRCLE_FORMATION = 0
    STATE_FREEZE = 1
    STATE_FIRE = 2

    def __init__(self, shooter: Enemy, angle: float, go_distance: float):
        self.origin_x = shooter.position[0] + math.cos(angle) * shooter.width/2
        self.origin_y = shooter.position[1] + math.sin(angle) * shooter.width/2
        super().__init__(RadialBullet.RADIUS, arcade.csscolor.VIOLET, self.origin_x, self.origin_y, angle, 300, shooter.stage)
        self.state = RadialBullet.STATE_CIRCLE_FORMATION
        self.go_distance = go_distance
    
    def go_fire(self, target_x: float, target_y: float):
        if target_y - self.position[1] == 0:
            if target_x > self.position[0]:
                self.angle = 0
            else:
                self.angle = math.pi
        else:
            slope = (self.position[0] - target_x) / (self.position[1] - target_y)
            self.angle = math.atan(slope)

    def on_update(self, delta_time: float):
        x = self.position[0]
        y = self.position[1]
        if self.state == RadialBullet.STATE_CIRCLE_FORMATION:
            if distance(x, y, self.origin_x, self.origin_y) < self.go_distance:
                x += math.cos(self.angle) * delta_time * self.speed
                y += math.sin(self.angle) * delta_time * self.speed
            else:
                self.state = RadialBullet.STATE_FREEZE
        elif self.state == RadialBullet.STATE_FIRE:
            x += math.cos(self.angle) * delta_time * self.speed
            y += math.sin(self.angle) * delta_time * self.speed
        
        self.set_position(x, y)


class Cartwheel(DartingEnemy):
    RADIUS = 15
    INIT_HP = 8

    def __init__(self, x: float, y: float, stage: Stage, interval: float = 2):
        super().__init__(Cartwheel.RADIUS, x, y, stage, Cartwheel.INIT_HP)
        self.next_x, self.next_y = self.position
    

    