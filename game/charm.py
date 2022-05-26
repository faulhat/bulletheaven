import math
import arcade

from stage import Stage
from utils import distance


class Charm(arcade.SpriteCircle):
    SPEED = 350
    ACCELERATION = 100
    RADIUS = 30
    COLOR = arcade.csscolor.GREENYELLOW

    def __init__(self, x: float, y: float, stage: Stage):
        super().__init__(Charm.RADIUS, Charm.COLOR)
        self.set_position(x, y)
        self.speed = Charm.SPEED
        self.stage = stage
        self.stage.charms.append(self)
        self.rect_width = math.sqrt(math.pow(Charm.RADIUS, 2) * 2)

    def on_update(self, delta_time: float):
        x, y = self.position
        player_x, player_y = self.stage.player.position
        if distance(x, y, player_x, player_y) < 100:
            angle = math.atan2(player_y - y, player_x - x)
            x += math.cos(angle) * delta_time * self.SPEED * 1.5
            y += math.sin(angle) * delta_time * self.SPEED * 1.5
        else:
            y -= self.speed * delta_time

        self.set_position(x, y)
        if y < 0:
            self.remove_from_sprite_lists()

        self.speed += Charm.ACCELERATION * delta_time

    def draw(self):
        arcade.draw_rectangle_filled(
            self.position[0],
            self.position[1],
            self.rect_width,
            self.rect_width,
            Charm.COLOR,
        )
