import math
import arcade

from bullets import Bullet
from enemy import Enemy, Boss
from l1enemies import DartingEnemy
from stage import Stage
from constants import *
from utils import distance


class RadialBullet(Bullet):
    STATE_CIRCLE_FORMATION = 0
    STATE_FREEZE = 1
    STATE_FIRE = 2
    SLOWING_RATE = 200

    def __init__(
        self,
        shooter: Enemy,
        angle: float,
        go_distance: float,
        speed: float = 1000,
        slowing_rate: float = None,
    ):
        self.origin_x = shooter.position[0] + math.cos(angle) * shooter.width / 2
        self.origin_y = shooter.position[1] + math.sin(angle) * shooter.width / 2
        if speed is None:
            speed = RadialBullet.INIT_SPEED

        if slowing_rate is None:
            slowing_rate = RadialBullet.SLOWING_RATE

        super().__init__(
            arcade.csscolor.VIOLET,
            self.origin_x,
            self.origin_y,
            angle,
            speed,
            shooter.stage,
        )
        self.state = RadialBullet.STATE_CIRCLE_FORMATION
        self.go_distance = go_distance
        self.slowing_rate = slowing_rate

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
            self.speed = max(100, self.speed - self.slowing_rate * delta_time)

    def remove_from_sprite_lists(self):
        self.state = RadialBullet.STATE_FREEZE
        super().remove_from_sprite_lists()


class Balloon(DartingEnemy):
    RADIUS = 15
    COLOR = arcade.csscolor.ALICE_BLUE
    INIT_HP = 15

    def __init__(
        self,
        x: float,
        y: float,
        stage: Stage,
        interval: float = 0.7,
        bullet_counts: list[int] = None,
        fire_radii: list[int] = None,
    ):
        super().__init__(
            Balloon.RADIUS, x, y, stage, Balloon.INIT_HP, interval=interval
        )
        self.bullet_counts = bullet_counts
        self.bullets_active = []
        self.shooting = False
        self.angle = 0
        if bullet_counts:
            self.bullet_counts = bullet_counts
        else:
            self.bullet_counts = [15]

        self.n_rounds = len(self.bullet_counts)
        if fire_radii:
            self.fire_radii = fire_radii
        else:
            self.fire_radii = [50 + i * 30 for i in range(self.n_rounds)]

        self.round = 0
        self.counter_in_round = 0
        self.waiting_on_round = 0

    def on_update(self, delta_time: float):
        if not self.shooting:
            if self.stopwatch > self.interval:
                self.stopwatch = 0
                self.shooting = True
            else:
                self.dart_update()
        else:
            if self.stopwatch > self.interval / self.bullet_counts[self.round]:
                self.stopwatch = 0
                if self.counter_in_round == self.bullet_counts[self.round]:
                    if self.round < self.n_rounds - 1:
                        self.counter_in_round = 0
                        self.round += 1
                elif self.round < self.n_rounds:
                    self.counter_in_round += 1
                    self.angle += math.pi * 2 / self.bullet_counts[self.round]
                    self.bullets_active.append(
                        RadialBullet(self, self.angle, self.fire_radii[self.round])
                    )

            bullet_count = self.bullet_counts[self.waiting_on_round]
            if len(self.bullets_active) >= bullet_count:
                all_bullets_out = True
                for bullet in self.bullets_active[:bullet_count]:
                    if bullet.state != RadialBullet.STATE_FREEZE:
                        all_bullets_out = False

                if all_bullets_out:
                    for bullet in self.bullets_active[:bullet_count]:
                        bullet.go_fire(*self.stage.player.position)

                    self.bullets_active = self.bullets_active[bullet_count:]
                    self.waiting_on_round += 1
                    if self.waiting_on_round == self.n_rounds:
                        self.round = 0
                        self.waiting_on_round = 0
                        self.counter_in_round = 0
                        self.bullets_active = []
                        self.shooting = False
                        self.rand_next()

        super().on_update(delta_time)

    def on_die(self):
        for bullet in self.bullets_active:
            bullet.go_fire(*self.stage.player.position)

        self.bullets_active = []
        super().on_die()


class Zeppelin(Balloon, Boss):
    COLOR = arcade.csscolor.WHITE_SMOKE
    BOSS_INIT_HP = 45
    NAME = "Zeppelin"

    def __init__(self, stage: Stage):
        Balloon.__init__(
            self,
            WIDTH / 3,
            HEIGHT + Balloon.RADIUS,
            stage,
            interval=0.5,
            bullet_counts=[15, 19, 22, 25],
            fire_radii=[50, 100, 125, 150],
        )

        Boss.__init__(self)

    def on_update(self, delta_time: float):
        Balloon.on_update(self, delta_time)
        self.update_hp_bar()
