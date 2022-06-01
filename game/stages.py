import arcade

from enemy import Boss
from l1enemies import SeaStar, FallingStar, Turret, Wormwood
from l2enemies import Balloon, Zeppelin
from l3enemies import AimingTurret, FireBomber, Wyvern
from bonusenemies import Gatling, Camazotz
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
        if self.stage_stopwatch.check_reset(7):
            self.make_dual_wielder()


class L1Stage3(Stage):
    def __init__(self, previous: Stage = None):
        super().__init__(previous)
        self.transition_label.text = "Level One - Stage Three"
        self.sea_stars = arcade.SpriteList()
        self.falling_stars = arcade.SpriteList()
        self.new_enemy_clock = self.new_stopwatch()
        self.new_enemy_wait = False
        self.counter = 0

    def inc_stage(self):
        self.window.show_view(L1Stage4(self))

    def make_falling_stars(self):
        dual_wielder_a = FallingStar(100, self)
        dual_wielder_b = FallingStar(HEIGHT - 100, self)
        self.falling_stars.append(dual_wielder_a)
        self.falling_stars.append(dual_wielder_b)

    def start_stage(self):
        super().start_stage()
        sea_star_a = SeaStar(WIDTH / 2 - 20, HEIGHT + 15, self, n_bullets=4)
        sea_star_b = SeaStar(WIDTH / 2 + 20, HEIGHT + 15, self, n_bullets=4)
        self.sea_stars.append(sea_star_a)
        self.sea_stars.append(sea_star_b)

        self.make_falling_stars()

    def stage_update(self, delta_time: float):
        if self.stage_stopwatch.check_reset(15):
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

        if not self.falling_stars:
            if not self.new_enemy_wait:
                self.new_enemy_wait = True
                self.new_enemy_clock.reset()
            elif self.new_enemy_clock.check(2):
                self.new_enemy_wait = False
                self.make_falling_stars()


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
            turret_a = Turret(HEIGHT * 4 / 8, RIGHT, self)
            turret_b = Turret(HEIGHT * 6 / 8, LEFT, self)
        else:
            turret_a = Turret(HEIGHT * 5 / 8, LEFT, self)
            turret_b = Turret(HEIGHT * 7 / 8, RIGHT, self)

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
        if not self.turrets:
            if not self.turrets_wait:
                self.turrets_wait = True
                self.counter += 1
                self.stage_stopwatch.reset()
            elif self.stage_stopwatch.check(3):
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
        self.intro_new_enemy_watch = self.new_stopwatch()
        self.new_enemy_introduced = False

    def inc_stage(self):
        self.window.show_view(L2Stage2(self))

    def start_stage(self):
        super().start_stage()
        Balloon(WIDTH / 3, HEIGHT + Balloon.RADIUS, self)

    def on_update(self, delta_time: float):
        super().on_update(delta_time)
        if not self.new_enemy_introduced:
            if self.intro_new_enemy_watch.check(1):
                Balloon(WIDTH * 2 / 3, HEIGHT + Balloon.RADIUS, self)
                self.new_enemy_introduced = True


class L2Stage2(Stage):
    def __init__(self, previous: Stage = None):
        super().__init__(previous)
        self.transition_label.text = "Level Two - Stage Two"

    def inc_stage(self):
        self.window.show_view(L2Stage3(self))

    def start_stage(self):
        super().start_stage()
        Balloon(WIDTH / 4, HEIGHT + Balloon.RADIUS, self, interval=1.5)
        Balloon(WIDTH * 3 / 4, HEIGHT + Balloon.RADIUS, self, interval=1.5)
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

        Balloon(
            WIDTH / 4,
            HEIGHT + Balloon.RADIUS,
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
        self.window.show_view(L3Stage1(self))

    def start_stage(self):
        super().start_stage()
        self.boss = Zeppelin(self)


class L3Stage1(Stage):
    def __init__(self, previous: Stage = None):
        super().__init__(previous)
        self.transition_label.text = "Level Three - Stage One"
        self.direction_switch = LEFT
        self.turret_counter = 0

    def make_turrets(self):
        Turret(HEIGHT * 3 / 4, self.direction_switch, self)
        self.direction_switch *= -1

    def inc_stage(self):
        self.window.show_view(L3Stage2(self))

    def start_stage(self):
        super().start_stage()
        FireBomber(
            WIDTH + FireBomber.RADIUS,
            HEIGHT + FireBomber.RADIUS,
            self,
            bullet_counts=[10, 12],
            interval=2,
        )

    def stage_update(self, delta_time: float):
        if self.enemies and self.stage_stopwatch.check_reset(
            (WIDTH + 50) / Turret.SPEED
        ):
            self.make_turrets()


class L3Stage2(Stage):
    def __init__(self, previous: Stage = None):
        super().__init__(previous)
        self.transition_label.text = "Level Three - Stage Two"
        self.direction_switch = LEFT

    def make_turrets(self):
        AimingTurret(HEIGHT * 6 / 8, self, self.direction_switch, n_bullets=3)
        AimingTurret(HEIGHT * 7 / 8, self, -self.direction_switch, n_bullets=3)
        self.direction_switch *= -1

    def inc_stage(self):
        self.window.show_view(L3Gauntlet(self))

    def start_stage(self):
        super().start_stage()
        FireBomber(
            -FireBomber.RADIUS,
            HEIGHT + FireBomber.RADIUS,
            self,
            bullet_counts=[10, 10, 10],
            interval=1.5,
        )

    def stage_update(self, delta_time: float):
        if self.enemies and self.stage_stopwatch.check_reset(7):
            self.make_turrets()


class L3Gauntlet(Stage):
    boss: Boss

    def __init__(self, previous: Stage = None):
        super().__init__(previous)
        self.transition_label.text = "Level Three - The Gauntlet"
        self.mode = 0
        self.direction_switch = LEFT

    def inc_stage(self):
        if self.mode > 6:
            self.window.show_view(L3Boss(self))
        else:
            self.next_mode()

    def start_stage(self):
        super().start_stage()
        SeaStar(
            WIDTH + SeaStar.RADIUS,
            HEIGHT + SeaStar.RADIUS,
            self,
            n_spines=6,
            double=True,
        )

    def next_mode(self):
        self.mode += 1
        if self.mode == 1:
            SeaStar(
                WIDTH + SeaStar.RADIUS,
                HEIGHT + SeaStar.RADIUS,
                self,
                n_spines=4,
                double=True,
            )
            SeaStar(
                -SeaStar.RADIUS, HEIGHT + SeaStar.RADIUS, self, n_spines=4, double=True
            )
        elif self.mode == 2:
            Balloon(
                WIDTH * 2 / 3,
                HEIGHT + Balloon.RADIUS,
                self,
                interval=1,
                bullet_counts=[15, 15, 15],
            )
        elif self.mode == 3:
            Balloon(
                WIDTH * 2 / 5,
                HEIGHT + Balloon.RADIUS,
                self,
                interval=1,
                bullet_counts=[15, 20],
            )
            Balloon(
                WIDTH * 3 / 5,
                HEIGHT + Balloon.RADIUS,
                self,
                interval=1,
                bullet_counts=[15, 20],
            )
        elif self.mode == 4:
            FireBomber(
                WIDTH / 2,
                HEIGHT + FireBomber.RADIUS,
                self,
                bullet_counts=[8, 10, 15, 20],
            )
        elif self.mode == 5:
            self.boss = Wormwood(self)
        elif self.mode == 6:
            self.boss = Zeppelin(self)

    def stage_update(self, delta_time: float):
        if self.enemies:
            if self.mode == 1:
                if self.stage_stopwatch.check_reset(10):
                    FallingStar(WIDTH * 1 / 2 + self.direction_switch * 200, self)
                    self.direction_switch *= -1
            elif self.mode == 2:
                if self.stage_stopwatch.check_reset(10):
                    Turret(HEIGHT * 3 / 4, self.direction_switch, self)
                    self.direction_switch *= -1
            elif self.mode == 5:
                if self.stage_stopwatch.check_reset(10):
                    FallingStar(WIDTH * 1 / 4, self)
                    FallingStar(WIDTH * 3 / 4, self)
            elif self.mode == 6:
                if self.stage_stopwatch.check_reset(8):
                    AimingTurret(WIDTH * 2 / 3, self, self.direction_switch)
                    self.direction_switch *= -1

        if self.mode == 5 or self.mode == 6:
            if self.boss.hp == 0:
                self.boss.hp_label.text = "Boss Vanquished!"

    def on_draw(self):
        super().on_draw()

        if self.mode == 5 or self.mode == 6:
            self.boss.draw_hp_bar()


class L3Boss(BossStage):
    def __init__(self, previous: Stage = None):
        super().__init__(previous)
        self.transition_label.text = "Level Three Boss - Wyvern"

    def inc_stage(self):
        self.window.show_view(ToEnd(self))

    def start_stage(self):
        super().start_stage()
        self.boss = Wyvern(self)


class BonusStage1(BossStage):
    def __init__(self, previous: Stage = None):
        super().__init__(previous)
        self.transition_label.text = "Bonus Stage One!"

    def inc_stage(self):
        self.window.show_view(ToEnd(self))

    def start_stage(self):
        super().start_stage()
        self.boss = Gatling(WIDTH + Gatling.RADIUS, HEIGHT + Gatling.RADIUS, self)


class BonusStage2(BossStage):
    def __init__(self, previous: Stage = None):
        super().__init__(previous)
        self.transition_label.text = "Bonus Stage Two!"

    def inc_stage(self):
        self.window.show_view(ToEnd(self))

    def start_stage(self):
        super().start_stage()
        self.boss = Camazotz(-Camazotz.RADIUS, HEIGHT + Camazotz.RADIUS, self)


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
