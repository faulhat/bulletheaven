import math
import arcade


# Forward declaration to prevent circular import
class Stage(arcade.View):
    friendly: arcade.SpriteList
    bullets: arcade.SpriteList


class Bullet(arcade.SpriteCircle):
    def __init__(
        self,
        radius: float,
        color: arcade.Color,
        x: float,
        y: float,
        angle: float,
        speed: float,
        stage: Stage,
        friendly: bool = False,
    ):
        super().__init__(radius, color)
        self.set_position(x, y)
        self.radius = radius
        self.angle = angle
        self.speed = speed
        self.stage = stage

        if friendly:
            stage.friendly.append(self)
        else:
            stage.bullets.append(self)

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
