import math
import arcade

from constants import *
from stopwatch import GameObject


# Forward declaration to prevent circular import
class Stage(arcade.View):
    friendly: arcade.SpriteList
    bullets: arcade.SpriteList


class Bullet(arcade.SpriteCircle, GameObject):
    RADIUS = 8

    def __init__(
        self,
        color: arcade.Color,
        x: float,
        y: float,
        angle: float,
        speed: float,
        stage: Stage,
        friendly: bool = False,
    ):
        arcade.SpriteCircle.__init__(self, Bullet.RADIUS, color)
        GameObject.__init__(self)

        self.set_position(x, y)
        self.angle = angle
        self.speed = speed
        self.stage = stage
        self.color = color

        if friendly:
            stage.friendly.append(self)
        else:
            stage.bullets.append(self)

    def out_of_bounds(self):
        x, y = self.position
        return (
            x > WIDTH + self.width / 2
            or x < -self.width / 2
            or y > HEIGHT + self.width / 2
            or y < -self.width / 2
        )

    def on_update(self, delta_time: float):
        self.add_all(delta_time)

        x = self.position[0] + math.cos(self.angle) * self.speed * delta_time
        y = self.position[1] + math.sin(self.angle) * self.speed * delta_time
        self.set_position(x, y)
        if self.out_of_bounds():
            self.remove_from_sprite_lists()

    def draw(self):
        arcade.draw_circle_outline(
            self.position[0],
            self.position[1],
            self.width / 2,
            self.color,
            border_width=2,
        )
