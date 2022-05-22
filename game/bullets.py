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
        stage: arcade.View,
    ):
        super().__init__(radius, color)
        self.set_position(x, y)
        self.radius = radius
        self.angle = angle
        self.speed = speed
        self.stage = stage

    def on_update(self, delta_time: float):
        x = self.position[0] + math.cos(self.angle) * self.speed * delta_time
        y = self.position[1] + math.sin(self.angle) * self.speed * delta_time
        self.set_position(x, y)

        if (
            x > self.stage.window.width + self.radius
            or x < -self.radius
            or y > self.stage.window.height + self.radius
            or y < -self.radius
        ):
            self.remove_from_sprite_lists()
