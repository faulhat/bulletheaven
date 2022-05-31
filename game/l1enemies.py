import math
from random import random
import arcade

from enemy import Enemy, Boss, DartingEnemy
from bullets import Bullet
from stage import Stage
from constants import *


class BasicBullet(Bullet):
    def __init__(self, x: float, y: float, angle: float, stage: Stage):
        super().__init__(arcade.csscolor.VIOLET, x, y, angle, 400, stage)


class SeaStar(DartingEnemy):
    RADIUS = 15
    COLOR = arcade.csscolor.PINK

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
        super().__init__(SeaStar.RADIUS, x, y, stage, 12, interval=interval)
        self.counter = 0
        self.angle_offset = 0
        self.n_spines = n_spines
        self.interval = interval
        self.n_bullets = n_bullets
        self.double = double

    def change_state(self):
        super().change_state()
        self.counter = 0

    def on_update(self, delta_time: float):
        super().on_update(delta_time)

        if not self.shooting:
            if self.dart_clock.check(self.interval):
                self.change_state()
            else:
                self.dart_update()
        else:
            if self.dart_clock.check_reset(self.interval / self.n_bullets):
                self.counter += 1
                if (not self.double and self.counter > self.n_bullets) or (
                    self.double and self.counter > self.n_bullets * 2
                ):
                    self.change_state()
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
    SPEED = 200
    COLOR = arcade.csscolor.DEEP_SKY_BLUE
    INIT_HP = 4

    angle: float

    def __init__(self, x: float, stage: Stage):
        super().__init__(15, x, HEIGHT + 10, stage, init_hp=FallingStar.INIT_HP)
        self.target_x = WIDTH - x
        self.target_y = -10
        self.fire_clock = self.new_stopwatch()

        if self.target_x - x == 0:
            # Avoid division by zero.
            self.angle = math.pi * 3 / 2
        else:
            self.angle = math.atan2(-(HEIGHT + 20), self.target_x - x)

    def on_update(self, delta_time: float):
        super().on_update(delta_time)

        if self.position[1] < self.target_y:
            self.remove_from_sprite_lists()
            return

        if self.fire_clock.check_reset(0.5):
            opp_angle = -self.angle + math.pi
            x = self.position[0] + math.cos(opp_angle)
            BasicBullet(x, self.position[1], opp_angle, self.stage)

        x = self.position[0] + math.cos(self.angle) * FallingStar.SPEED * delta_time
        y = self.position[1] + math.sin(self.angle) * FallingStar.SPEED * delta_time
        self.set_position(x, y)


class Turret(Enemy):
    RADIUS = 15
    COLOR = arcade.csscolor.GREENYELLOW
    INIT_HP = 4
    SPEED = 250

    def __init__(
        self,
        y: float,
        direction: int,
        stage: Stage,
    ):
        super().__init__(12, 0, y, stage, init_hp=Turret.INIT_HP)
        x: float
        if direction == LEFT:
            x = WIDTH + Turret.RADIUS
        elif direction == RIGHT:
            x = -Turret.RADIUS

        self.set_position(x, y)
        self.speed = Turret.SPEED

        self.direction = direction
        self.fire_clock = self.new_stopwatch()

    def on_update(self, delta_time: float):
        super().on_update(delta_time)

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

        if self.fire_clock.check_reset(0.3):
            BasicBullet(
                x,
                y - self.width / 2,
                math.pi * 3 / 2,
                self.stage,
            )


class Wormwood(SeaStar, Boss):
    BOSS_INIT_HP = 40
    COLOR = arcade.csscolor.BEIGE
    NAME = "Wormwood"
    SPEED = 400

    def __init__(self, stage: Stage):
        SeaStar.__init__(
            self,
            WIDTH * 2 / 3,
            HEIGHT + SeaStar.RADIUS,
            stage,
            n_spines=7,
            interval=0.75,
            double=True,
        )

        Boss.__init__(self)
        self.fire_star = True
        self.crossing_direction = LEFT
        self.turret_fire_clock = self.new_stopwatch()

    def change_state(self):
        self.reset_all()
        self.shooting = not self.shooting
        if not self.shooting:
            self.fire_star = not self.fire_star
            if self.fire_star:
                self.rand_next()
                self.counter = 0
        else:
            if not self.fire_star:
                self.crossing_direction *= -1

    def on_update(self, delta_time: float):
        if self.shooting:
            x, y = self.position
            x += (2 * random() - 1) * delta_time * Wormwood.SPEED / 4
            y += (2 * random() - 1) * delta_time * Wormwood.SPEED / 4
            self.set_position(x, y)

        if self.fire_star:
            SeaStar.on_update(self, delta_time)
        else:
            Enemy.on_update(self, delta_time)

            x, y = self.position
            x += Wormwood.SPEED * delta_time * self.crossing_direction
            if self.crossing_direction == LEFT and x <= Wormwood.RADIUS:
                x = Wormwood.RADIUS
                self.change_state()
            elif self.crossing_direction == RIGHT and x >= WIDTH - Wormwood.RADIUS:
                x = WIDTH - Wormwood.RADIUS
                self.change_state()

            self.set_position(x, y)
            if self.shooting and self.turret_fire_clock.check_reset(0.35):
                BasicBullet(
                    self.position[0],
                    y - Wormwood.RADIUS - BasicBullet.RADIUS,
                    math.pi * 3 / 2,
                    self.stage,
                )

        self.update_hp_bar()
