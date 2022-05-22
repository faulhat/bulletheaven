import arcade

from enemies import SeaStar, DualWielder
from stage import Stage, Player
from youwin import YouWin


class StageOne(Stage):
    def __init__(self, player: Player):
        super().__init__(player, 1, set())

    def inc_stage(self):
        self.window.show_view(StageTwo(self.player, self.keys))

    def start_stage(self):
        super().start_stage()
        SeaStar(100, self.window.height + 15, self)
        SeaStar(self.window.width - 100, self.window.height + 15, self)

    def stage_update(self, delta_time: float):
        super().stage_update(delta_time)


class StageTwo(Stage):
    def __init__(self, player: Player, keys: set):
        super().__init__(player, 2, keys)

    def inc_stage(self):
        self.window.show_view(StageThree(self.player, self.keys))

    def start_stage(self):
        super().start_stage()
        SeaStar(self.window.width / 2, self.window.height + 15, self, n_spines=8)
        DualWielder(50, self)
        DualWielder(self.window.width - 50, self)

    def stage_update(self, delta_time: float):
        super().stage_update(delta_time)
        if self.stage_stopwatch > 7:
            self.stage_stopwatch = 0
            DualWielder(50, self)
            DualWielder(self.window.width - 50, self)


class StageThree(Stage):
    def __init__(self, player: Player, keys: set):
        super().__init__(player, 3, keys)

    def inc_stage(self):
        self.window.show_view(StageFour(self.player, self.keys))

    def start_stage(self):
        super().start_stage()
        SeaStar(self.window.width / 2 - 20, self.window.height + 15, self)
        SeaStar(self.window.width / 2 + 20, self.window.height + 15, self)
        DualWielder(self.window.width / 2, self)
        DualWielder(100, self)
        DualWielder(self.window.height - 100, self)

    def stage_update(self, delta_time: float):
        super().stage_update(delta_time)
        if self.stage_stopwatch > 10:
            self.stage_stopwatch = 0
            if len(self.enemies) == 1:
                SeaStar(self.window.width / 2, self.window.height + 15, self)


class StageFour(Stage):
    def __init__(self, player: Player, keys: set):
        super().__init__(player, 4, keys)

    def inc_stage(self):
        pass

    def start_stage(self):
        self.window.show_view(YouWin())

    def stage_update(self, delta_time: float):
        return super().stage_update(delta_time)

    def on_draw(self):
        self.player.draw()
