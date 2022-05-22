import math
import arcade

from stage import Stage
from enemies import SimpleEnemy


class StageOne(Stage):
    def __init__(self):
        super().__init__()
        self.enemies.append(SimpleEnemy(500, 500, self))
