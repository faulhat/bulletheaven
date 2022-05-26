import math
import arcade

from stage import Stage
from utils import distance

class Charm(arcade.SpriteSolidColor):
    SPEED = 350
    ACCELERATION = 100

    def __init__(self, x: float, y: float, stage: Stage):
        super().__init__(35, 35, arcade.csscolor.GREENYELLOW)
        self.set_position(x, y)
        self.speed = Charm.SPEED
        self.stage = stage
        self.stage.charms.append(self)

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
