import arcade

from l1enemies import SeaStar, FallingStar, Turret, Wormwood
from l2enemies import Bomber, Zeppelin
from stage import Stage, BossStage
from gameover import YouWin
from constants import *


class L1Stage1(Stage):
    def __init__(self, previous: Stage = None):
        super().__init__(previous)
        self.transition_label.text = "Level One - Stage One"

    def inc_stage(self):
        self.window.show_view(L1Stage2(self))

    def start_stage(self):
        super().start_stage()
        SeaStar(100, HEIGHT + 15, self, interval=2)
        SeaStar(
            WIDTH - 100,
            HEIGHT + 15,
            self,
            interval=2,
        )

    def stage_update(self, delta_time: float):
        super().stage_update(delta_time)


class L1Stage2(Stage):
    def __init__(self, previous: Stage = None):
        super().__init__(previous)
        self.transition_label.text = "Level One - Stage Two"
        self.switch = False

    def inc_stage(self):
        self.window.show_view(L1Stage3(self))

    def make_dual_wielder(self):
        if self.switch:
            FallingStar(50, self)
        else:
            FallingStar(WIDTH - 50, self)

        self.switch = not self.switch

    def start_stage(self):
        super().start_stage()
        SeaStar(WIDTH / 2, HEIGHT + 15, self, n_spines=8)
        self.make_dual_wielder()

    def stage_update(self, delta_time: float):
        super().stage_update(delta_time)
        if self.stage_stopwatch > 7:
            self.stage_stopwatch = 0
            self.make_dual_wielder()


class L1Stage3(Stage):
    def __init__(self, previous: Stage = None):
        super().__init__(previous)
        self.transition_label.text = "Level One - Stage Three"
        self.sea_stars = arcade.SpriteList()
        self.dual_wielders = arcade.SpriteList()
        self.new_enemy_clock = 0
        self.new_enemy_wait = False
        self.counter = 0

    def inc_stage(self):
        self.window.show_view(L1Stage4(self))

    def make_dual_wielders(self):
        dual_wielder_a = FallingStar(100, self)
        dual_wielder_b = FallingStar(HEIGHT - 100, self)
        self.dual_wielders.append(dual_wielder_a)
        self.dual_wielders.append(dual_wielder_b)

    def start_stage(self):
        super().start_stage()
        sea_star_a = SeaStar(WIDTH / 2 - 20, HEIGHT + 15, self, n_bullets=4)
        sea_star_b = SeaStar(WIDTH / 2 + 20, HEIGHT + 15, self, n_bullets=4)
        self.sea_stars.append(sea_star_a)
        self.sea_stars.append(sea_star_b)

        self.make_dual_wielders()

    def stage_update(self, delta_time: float):
        super().stage_update(delta_time)
        if self.stage_stopwatch > 15:
            self.stage_stopwatch = 0
            if len(self.sea_stars) == 1 and self.counter < 2:
                self.counter += 1
                self.sea_stars.append(
                    SeaStar(
                        WIDTH / 2,
                        HEIGHT + 15,
                        self,
                        n_bullets=4,
                    )
                )

        self.new_enemy_clock += delta_time
        if len(self.dual_wielders) == 0:
            if not self.new_enemy_wait:
                self.new_enemy_wait = True
                self.new_enemy_clock = 0
            elif self.new_enemy_clock > 2:
                self.new_enemy_wait = False
                self.make_dual_wielders()


class L1Stage4(Stage):
    def __init__(self, previous: Stage = None):
        super().__init__(previous)
        self.transition_label.text = "Level One - Stage Four"

        self.counter = 0
        self.turrets = arcade.SpriteList()
        self.turrets_wait = False

    def inc_stage(self):
        self.window.show_view(L1Boss(self))

    def make_turrets(self):
        turret_a: Turret
        turret_b: Turret
        if self.counter % 2 == 0:
            turret_a = Turret(HEIGHT * 4 / 8, Turret.RIGHT, 400, self)
            turret_b = Turret(HEIGHT * 6 / 8, Turret.LEFT, 400, self)
        else:
            turret_a = Turret(HEIGHT * 5 / 8, Turret.LEFT, 400, self)
            turret_b = Turret(HEIGHT * 7 / 8, Turret.RIGHT, 400, self)

        self.turrets.append(turret_a)
        self.turrets.append(turret_b)

    def start_stage(self):
        super().start_stage()
        miniboss = SeaStar(
            WIDTH / 3,
            HEIGHT + SeaStar.RADIUS,
            self,
            2,
            interval=1.5,
            n_bullets=7,
            double=True,
        )
        miniboss.hp = 20

        self.make_turrets()

    def stage_update(self, delta_time: float):
        super().stage_update(delta_time)

        if len(self.turrets) == 0:
            if not self.turrets_wait:
                self.turrets_wait = True
                self.counter += 1
                self.stage_stopwatch = 0
            elif self.stage_stopwatch > 3:
                self.turrets_wait = False
                self.make_turrets()


class L1Boss(BossStage):
    def __init__(self, previous: Stage = None):
        super().__init__(previous)
        self.transition_label.text = "Level One Boss - Wormwood"

    def inc_stage(self):
        self.window.show_view(L2Stage1(self))

    def start_stage(self):
        super().start_stage()
        self.boss = Wormwood(self)


class L2Stage1(Stage):
    def __init__(self, previous: Stage = None):
        super().__init__(previous)
        self.transition_label.text = "Level Two - Stage One"
        self.intro_new_enemy_watch = 0
        self.new_enemy_introduced = False

    def inc_stage(self):
        self.window.show_view(L2Stage2(self))

    def start_stage(self):
        super().start_stage()
        Bomber(WIDTH / 3, HEIGHT + Bomber.RADIUS, self)

    def on_update(self, delta_time: float):
        super().on_update(delta_time)
        if not self.new_enemy_introduced:
            self.intro_new_enemy_watch += delta_time

            if self.intro_new_enemy_watch > 1:
                Bomber(WIDTH * 2 / 3, HEIGHT + Bomber.RADIUS, self)
                self.new_enemy_introduced = True


class L2Stage2(Stage):
    def __init__(self, previous: Stage = None):
        super().__init__(previous)
        self.transition_label.text = "Level Two - Stage Two"

    def inc_stage(self):
        self.window.show_view(L2Stage3(self))

    def start_stage(self):
        super().start_stage()
        Bomber(WIDTH / 4, HEIGHT + Bomber.RADIUS, self, interval=1.5)
        Bomber(WIDTH * 3 / 4, HEIGHT + Bomber.RADIUS, self, interval=1.5)
        SeaStar(WIDTH / 3, HEIGHT + SeaStar.RADIUS, self)


class L2Stage3(L1Stage2):
    def __init__(self, previous: Stage = None):
        super().__init__(previous)
        self.transition_label.text = "Level Two - Stage Three"

    def inc_stage(self):
        self.window.show_view(L2Boss(self))

    def start_stage(self):
        Stage.start_stage(self)

        SeaStar(
            WIDTH * 3 / 4,
            HEIGHT + SeaStar.RADIUS,
            self,
            n_spines=3,
            n_bullets=5,
        )

        Bomber(
            WIDTH / 4,
            HEIGHT + Bomber.RADIUS,
            self,
            bullet_counts=[6, 6],
        )

    def stage_update(self, delta_time: float):
        super().stage_update(delta_time)


class L2Boss(BossStage):
    def __init__(self, previous: Stage = None):
        super().__init__(previous)
        self.transition_label.text = "Level Two Boss - Zeppelin"

    def inc_stage(self):
        self.window.show_view(ToEnd(self))

    def start_stage(self):
        super().start_stage()
        self.boss = Zeppelin(self)


class ToEnd(Stage):
    def __init__(self, previous: Stage = None):
        super().__init__(previous)
        self.transition_label.text = "The End."

    def inc_stage(self):
        pass

    def start_stage(self):
        self.window.show_view(YouWin())

    def stage_update(self, delta_time: float):
        super.stage_update(delta_time)
