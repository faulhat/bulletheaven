import arcade

from enemies import SeaStar, FallingStar, Turret
from stage import Stage
from gameover import YouWin
from constants import *


class L1Stage1(Stage):
    def __init__(self):
        super().__init__()
        self.transition_label.text = "Level One - Stage One"

    def inc_stage(self):
        self.window.show_view(L1Stage2(self))

    def start_stage(self):
        super().start_stage()
        SeaStar(100, self.window.height + 15, self, interval=2)
        SeaStar(
            WIDTH - 100,
            self.window.height + 15,
            self,
            interval=2,
        )

    def stage_update(self, delta_time: float):
        super().stage_update(delta_time)


class L1Stage2(Stage):
    def __init__(self, previous: Stage):
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
        SeaStar(WIDTH / 2, self.window.height + 15, self, n_spines=8)
        self.make_dual_wielder()

    def stage_update(self, delta_time: float):
        super().stage_update(delta_time)
        if self.stage_stopwatch > 7:
            self.stage_stopwatch = 0
            self.make_dual_wielder()


class L1Stage3(Stage):
    def __init__(self, previous: Stage):
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
        dual_wielder_b = FallingStar(self.window.height - 100, self)
        self.dual_wielders.append(dual_wielder_a)
        self.dual_wielders.append(dual_wielder_b)

    def start_stage(self):
        super().start_stage()
        sea_star_a = SeaStar(
            WIDTH / 2 - 20, self.window.height + 15, self, n_bullets=4
        )
        sea_star_b = SeaStar(
            WIDTH / 2 + 20, self.window.height + 15, self, n_bullets=4
        )
        self.sea_stars.append(sea_star_a)
        self.sea_stars.append(sea_star_b)

        self.make_dual_wielders()

    def stage_update(self, delta_time: float):
        super().stage_update(delta_time)
        if self.stage_stopwatch > 15:
            self.stage_stopwatch = 0
            if len(self.sea_stars) == 1 and self.counter < 3:
                self.counter += 1
                self.sea_stars.append(
                    SeaStar(
                        WIDTH / 2,
                        self.window.height + 15,
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
    def __init__(self, previous: Stage):
        super().__init__(previous)
        self.transition_label.text = "Level One - Stage Four"

        self.counter = 0
        self.turrets = arcade.SpriteList()
        self.turrets_wait = False
        self.stage_stopwatch = 0

    def inc_stage(self):
        self.window.show_view(L1BossStage(self))

    def make_turrets(self):
        turret_a: Turret
        turret_b: Turret
        if self.counter % 2 == 0:
            turret_a = Turret(
                self.window.height * 4 / 8, Turret.RIGHT, 600, 20, 2, self
            )
            turret_b = Turret(self.window.height * 6 / 8, Turret.LEFT, 600, 20, 2, self)
        else:
            turret_a = Turret(self.window.height * 5 / 8, Turret.LEFT, 600, 20, 2, self)
            turret_b = Turret(
                self.window.height * 7 / 8, Turret.RIGHT, 600, 20, 2, self
            )

        self.turrets.append(turret_a)
        self.turrets.append(turret_b)

    def start_stage(self):
        super().start_stage()
        miniboss = SeaStar(
            WIDTH / 3,
            self.window.height + SeaStar.RADIUS,
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


class L1Boss(SeaStar):
    INIT_HP = 30
    HP_BAR_HEIGHT = 30

    def __init__(self, stage: Stage):
        super().__init__(
            stage.window.width * 2 / 3,
            stage.window.height + SeaStar.RADIUS,
            stage,
            n_bullets=5,
            interval=0.7,
            double=True,
        )

        self.hp = L1Boss.INIT_HP
        self.hp_label = arcade.Text(
            f"Boss HP: {L1Boss.INIT_HP}",
            20,
            self.stage.window.height - L1Boss.HP_BAR_HEIGHT / 2,
            arcade.csscolor.RED,
            font_size=18,
            font_name="PressStart2P",
            anchor_y="center",
        )

    def on_update(self, delta_time: float):
        super().on_update(delta_time)
        self.hp_label.text = f"Boss HP: {self.hp}"

    def draw_hp_bar(self):
        arcade.draw_rectangle_filled(
            self.hp / L1Boss.INIT_HP * WIDTH / 2,
            self.stage.window.height - L1Boss.HP_BAR_HEIGHT / 2,
            self.hp / L1Boss.INIT_HP * WIDTH,
            L1Boss.HP_BAR_HEIGHT,
            arcade.csscolor.GREEN,
        )

        self.hp_label.draw()


class L1BossStage(Stage):
    boss: L1Boss

    def __init__(self, previous):
        super().__init__(previous)
        self.transition_label.text = "Level One - Boss Battle!"

    def inc_stage(self):
        self.window.show_view(ToEnd(self))

    def start_stage(self):
        super().start_stage()
        self.boss = L1Boss(self)

    def stage_update(self, delta_time: float):
        super().stage_update(delta_time)
        if self.boss.hp == 0:
            self.boss.hp_label.text = "Boss Vanquished!"

    def on_draw(self):
        super().on_draw()
        if not self.in_transition:
            self.boss.draw_hp_bar()


class ToEnd(Stage):
    def __init__(self, previous: Stage):
        super().__init__(previous)
        self.transition_label.text = "The End."

    def inc_stage(self):
        pass

    def start_stage(self):
        self.window.show_view(YouWin())

    def stage_update(self, delta_time: float):
        super.stage_update(delta_time)
