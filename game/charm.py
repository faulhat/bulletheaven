import arcade

from stage import Stage

class Charm(arcade.SpriteSolidColor):
    SPEED = 400
    ACCELERATION = 100

    def __init__(self, x: float, y: float, stage: Stage):
        super().__init__(35, 35, arcade.csscolor.GREENYELLOW)
        self.set_position(x, y)
        self.speed = Charm.SPEED
        stage.charms.append(self)

    def on_update(self, delta_time: float):
        x, y = self.position
        y -= self.speed * delta_time
        self.set_position(x, y)
        if y < 0:
            self.remove_from_sprite_lists()

        self.speed += Charm.ACCELERATION * delta_time
