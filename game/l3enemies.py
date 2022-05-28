import math
from random import random
import arcade

from enemy import Enemy, Boss
from l1enemies import BasicBullet, DartingEnemy
from l2enemies import RadialBullet
from stage import Stage
from constants import *


class AimingTurret(Enemy):
    RADIUS = 15
    INIT_HP = 4
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

                if self.counter == self.n_bullets:
                    self.counter = 0
                    self.shooting = False
        else:
            if self.fire_watch > 0.5:
                self.fire_watch = 0
                self.shooting = True

        if self.direction == LEFT:
            x -= AimingTurret.SPEED * delta_time
            if x < -AimingTurret.RADIUS:
                self.remove_from_sprite_lists()
        elif self.direction == RIGHT:
            x += AimingTurret.SPEED * delta_time
            if x > WIDTH + AimingTurret.RADIUS:
                self.remove_from_sprite_lists()

        self.set_position(x, y)


class FireBomber(DartingEnemy):
    RADIUS = 15
    INIT_HP = 11
    COLOR = arcade.csscolor.ORANGE

    def __init__(
        self,
        x: float,
        y: float,
        stage: Stage,
        interval: float = 1,
        bullet_counts: list[int] = None,
        fire_radii: list[int] = None,
    ):
        super().__init__(
            FireBomber.RADIUS, x, y, stage, FireBomber.INIT_HP, interval=interval
        )
        self.bullet_counts = bullet_counts
        self.shooting = False
        self.bullets_active = []
        self.round = 0
        if bullet_counts:
            self.bullet_counts = bullet_counts
        else:
            self.bullet_counts = [10]

        self.n_rounds = len(self.bullet_counts)
        if fire_radii:
            self.fire_radii = fire_radii
        else:
            self.fire_radii = [50 + 10 * i for i in range(self.n_rounds)]

    def change_state(self):
        super().change_state()
        self.round = 0

    def on_update(self, delta_time: float):
        if not self.shooting:
            if self.stopwatch > self.interval:
                self.change_state()
            else:
                self.dart_update()
        else:
            fire_radius = self.fire_radii[self.round]
            bullet_count = self.bullet_counts[self.round]
            if not self.bullets_active:
                angle = random() * math.pi * 2
                for _ in range(bullet_count):
                    angle += math.pi * 2 / bullet_count
                    self.bullets_active.append(
                        RadialBullet(
                            self, angle, fire_radius, speed=400, slowing_rate=0
                        )
                    )
            else:
                bullets_out = True
                for bullet in self.bullets_active:
                    if bullet.state != RadialBullet.STATE_FREEZE:
                        bullets_out = False

                if bullets_out:
                    x, y = self.position
                    off_x, off_y = (random() * 2 - 1) * fire_radius, (
                        random() * 2 - 1
                    ) * fire_radius
                    for bullet in self.bullets_active:
                        bullet.go_fire(x + off_x, y + off_y)

                    self.bullets_active = []
                    self.round += 1
                    if self.round == self.n_rounds:
                        self.change_state()

        super().on_update(delta_time)

    def on_die(self):
        for bullet in self.bullets_active:
            bullet.go_fire(*self.position)

        self.bullets_active = []
        super().on_die()


class Wyvern(FireBomber, Boss):
    COLOR = arcade.csscolor.LIGHT_GREY
    BOSS_INIT_HP = 55
    NAME = "Wyvern"
    SPEED = 100

    def __init__(self, stage: Stage):
        FireBomber.__init__(
            self,
            WIDTH / 8,
            HEIGHT + FireBomber.RADIUS,
            stage,
            interval=1.2,
            bullet_counts=[20, 20, 15, 15, 15],
            fire_radii=[50, 50, 60, 70, 80],
        )

        Boss.__init__(self)
        self.fire_bomb = False
        self.counter = 0

    def change_state(self):
        if self.shooting and not self.fire_bomb:
            self.fire_bomb = True
            self.counter = 0
        else:
            super().change_state()
            self.fire_bomb = False

    def on_update(self, delta_time: float):
        if self.shooting:
            x, y = self.position
            x += (2 * random() - 1) * delta_time * Wyvern.SPEED
            y += (2 * random() - 1) * delta_time * Wyvern.SPEED
            self.set_position(x, y)

        if self.fire_bomb or not self.shooting:
            FireBomber.on_update(self, delta_time)
        else:
            Enemy.on_update(self, delta_time)
            self.stopwatch += delta_time

            if self.stopwatch > 0.2:
                self.stopwatch = 0
                self.counter += 1
                angle = random() * math.pi * 2
                x, y = self.position
                for _ in range(7):
                    bullet_x = x + math.cos(angle) * (
                        FireBomber.RADIUS + BasicBullet.RADIUS
                    )
                    bullet_y = y + math.sin(angle) * (
                        FireBomber.RADIUS + BasicBullet.RADIUS
                    )
                    BasicBullet(bullet_x, bullet_y, angle, self.stage)
                    angle += math.pi * 2 / 5

                if self.counter == 9:
                    self.change_state()

        self.update_hp_bar()
