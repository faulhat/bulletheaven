from abc import abstractmethod
import math
import arcade


class Bullet(arcade.SpriteCircle):
    def __init__(
        self,
        radius: float,
        color: arcade.Color,
        x: float,
        y: float,
        angle: float,
        speed: float,
    ):
        super().__init__(radius, color)
        self.set_position(x, y)
        self.angle = angle
        self.speed = speed

    def on_update(self, delta_time: float):
        x = self.position[0] + math.cos(self.angle) * self.speed * delta_time
        y = self.position[1] + math.sin(self.angle) * self.speed * delta_time
        self.set_position(x, y)
