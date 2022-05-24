import arcade

from gameover import YouWin
from stage import Stage
from l2enemies import CircleFire
from constants import *


class L2Stage1(Stage):
    def __init__(self, previous: Stage = None):
        super().__init__(previous)

    def inc_stage(self):
        self.window.show_view(YouWin())

    def start_stage(self):
        super().start_stage()
        CircleFire(WIDTH / 2, HEIGHT + CircleFire.RADIUS, self)
