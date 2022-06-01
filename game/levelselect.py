from menus import MenuItem, MenuItems, Menu
from stage import Stage
from stages import *
from constants import *


class Levels(MenuItems):
    def __init__(self, stages: list[Stage], start_y: int):
        self.stages = stages

        items = []
        for i, stage in enumerate(stages):
            start_y -= 30
            items.append(
                MenuItem(
                    stage.transition_label.text,
                    lambda view, i=i: view.window.show_view(self.stages[i]),
                    start_x=LevelSelect.LEFT_X,
                    start_y=start_y,
                    font_name="PressStart2P",
                    font_size=14,
                )
            )

        super().__init__(items)


class LevelSelect(Menu):
    START_Y = HEIGHT - 100
    LEFT_X = 100

    def __init__(self):
        LEVELS = [
            L1Stage1(),
            L1Stage2(),
            L1Stage3(),
            L1Stage4(),
            L1Boss(),
            L2Stage1(),
            L2Stage2(),
            L2Boss(),
            L3Stage1(),
            L3Stage2(),
            L3Gauntlet(),
            L3Boss(),
            BonusStage1(),
            BonusStage2(),
        ]

        super().__init__()
        self.options = Levels(LEVELS, LevelSelect.START_Y)
        self.menu_label = arcade.Text(
            "Select stage:",
            LevelSelect.LEFT_X,
            LevelSelect.START_Y,
            font_name="PressStart2P",
            font_size=14,
        )

    def on_draw(self):
        self.menu_label.draw()
        super().on_draw()
