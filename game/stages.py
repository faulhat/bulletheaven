import arcade

from enemies import SeaStar, DualWielder, Turret
from stage import Stage, Player
from youwin import YouWin


class StageOne(Stage):
    def __init__(self):
        super().__init__()
        self.transition_label.text = "Level One - Stage One"

    def inc_stage(self):
        self.window.show_view(StageTwo(self))

    def start_stage(self):
        super().start_stage()
        SeaStar(100, self.window.height + 15, self)
        SeaStar(self.window.width - 100, self.window.height + 15, self)

    def stage_update(self, delta_time: float):
        super().stage_update(delta_time)


class StageTwo(Stage):
    def __init__(self, previous: Stage):
        super().__init__(previous)
        self.transition_label.text = "Level One - Stage Two"

    def inc_stage(self):
        self.window.show_view(StageThree(self))

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
    def __init__(self, previous: Stage):
        super().__init__(previous)
        self.transition_label.text = "Level One - Stage Three"
        self.sea_stars = arcade.SpriteList()
        self.dual_wielders = arcade.SpriteList()
        self.new_enemy_clock = 0
        self.new_enemy_wait = False

    def inc_stage(self):
        self.window.show_view(StageFour(self))

    def make_dual_wielders(self):
        dual_wielder_a = DualWielder(100, self)
        dual_wielder_b = DualWielder(self.window.height - 100, self)
        self.dual_wielders.append(dual_wielder_a)
        self.dual_wielders.append(dual_wielder_b)

    def start_stage(self):
        super().start_stage()
        sea_star_a = SeaStar(self.window.width / 2 - 20, self.window.height + 15, self)
        sea_star_b = SeaStar(self.window.width / 2 + 20, self.window.height + 15, self)
        self.sea_stars.append(sea_star_a)
        self.sea_stars.append(sea_star_b)

        self.make_dual_wielders()

    def stage_update(self, delta_time: float):
        super().stage_update(delta_time)
        if self.stage_stopwatch > 15:
            self.stage_stopwatch = 0
            if len(self.sea_stars) == 1:
                SeaStar(self.window.width / 2, self.window.height + 15, self)
        
        self.new_enemy_clock += delta_time
        if len(self.dual_wielders) == 0:
            if not self.new_enemy_wait:
                self.new_enemy_wait = True
                self.new_enemy_clock = 0
            elif self.new_enemy_clock > 2:
                self.new_enemy_wait = False
                self.make_dual_wielders()


class StageFour(Stage):
    boss: SeaStar
    
    def __init__(self, previous: Stage):
        super().__init__(previous)
        self.transition_label.text = "Level One BOSS"

        self.counter = 0
        self.turrets = arcade.SpriteList()
        self.turrets_wait = False
        self.stage_stopwatch = 0
    
    def inc_stage(self):
        self.window.show_view(ToEnd(self))
    
    def make_turrets(self):
        turret_a: Turret
        turret_b: Turret
        if self.counter % 2 == 0:
            turret_a = Turret(self.window.height * 4/8, Turret.RIGHT, 600, 20, 2, self)
            turret_b = Turret(self.window.height * 6/8, Turret.LEFT, 600, 20, 2, self)
        else:
            turret_a = Turret(self.window.height * 5/8, Turret.LEFT, 600, 20, 2, self)
            turret_b = Turret(self.window.height * 7/8, Turret.RIGHT, 600, 20, 2, self)

        self.turrets.append(turret_a)
        self.turrets.append(turret_b)

    def start_stage(self):
        super().start_stage()
        self.boss = SeaStar(self.window.width / 3, self.window.height + SeaStar.RADIUS, self, 3)
        self.boss.hp = 35
        
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


class ToEnd(Stage):
    def __init__(self, previous: Stage):
        super().__init__(previous)
        self.transition_label.text = "The End."

    def inc_stage(self):
        pass

    def start_stage(self):
        self.window.show_view(YouWin())

    def stage_update(self, delta_time: float):
        return super().stage_update(delta_time)
