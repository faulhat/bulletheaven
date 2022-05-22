import arcade


class Player(arcade.SpriteCircle):
    def __init__(self):
        super().__init__(15, arcade.csscolor.ALICE_BLUE)
        self.hp = 5
        self.speed = 500
