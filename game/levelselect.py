from black import main
import mainmenu
from menus import MenuItem, MenuItems, Menu
from stage import Stage
from stages import *
from constants import *


class Levels(MenuItems):
    DESC_INTERVAL = 30

    def __init__(self, stages: list[Stage], start_y: int):
        self.stages = stages

        items = []
        for i, stage in enumerate(stages):
            start_y -= Levels.DESC_INTERVAL
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
            # BonusStage3(),
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

        option_return = MenuItem(
            "Go back",
            lambda view: view.window.show_view(mainmenu.MainMenu()),
            start_x=LevelSelect.LEFT_X,
            start_y=LevelSelect.START_Y - (1 + len(LEVELS)) * Levels.DESC_INTERVAL,
            font_name="PressStart2P",
            font_size=14,
        )
        self.options.items.append(option_return)

    def on_draw(self):
        self.menu_label.draw()
        super().on_draw()
