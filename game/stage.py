from abc import abstractmethod
import arcade

from contmenu import ContinueMenu
from gameover import GameOver
from pausemenu import PauseMenu
from player import Player
from constants import *


class Stage(arcade.View):
    def __init__(self, other: "Stage" = None):
        super().__init__()
        if not other:
            self.player = Player(
                WIDTH / 2,
                HEIGHT / 3,
                self,
            )
            self.enemies = arcade.SpriteList()

            # Sprite list for enemy bullets
            self.bullets = arcade.SpriteList()

            # Sprite list for the player's bullets
            self.friendly = arcade.SpriteList()

            # Sprite list for charms
            self.charms = arcade.SpriteList()

            self.keys = set()
        else:
            self.player = other.player
            self.enemies = other.enemies
            self.bullets = other.bullets
            self.friendly = other.friendly
            self.charms = other.charms
            self.keys = other.keys

            self.player.stage = self
            self.player.exit_serene_mode()

        self.stopwatch = 0
        self.stage_stopwatch = 0
        self.transition_label = arcade.Text(
            "",
            WIDTH / 2,
            HEIGHT / 2,
            font_size=20,
            anchor_x="center",
            anchor_y="center",
            font_name="PressStart2P",
        )
        self.in_transition = True

    @abstractmethod
    def inc_stage(self):
        pass

    @abstractmethod
    def start_stage(self):
        self.in_transition = False
        self.stage_stopwatch = 0

    @abstractmethod
    def stage_update(self, delta_time: float):
        self.stage_stopwatch += delta_time

    def on_key_press(self, symbol: int, modifiers: int):
        if symbol == arcade.key.X:
            self.window.show_view(PauseMenu(self))
            return

        if symbol == arcade.key.Q:
            self.player.use_charm()

        self.keys.add(symbol)
        return super().on_key_press(symbol, modifiers)

    def on_key_release(self, _symbol: int, _modifiers: int):
        self.keys.discard(_symbol)
        return super().on_key_release(_symbol, _modifiers)

    def on_update(self, delta_time: float):
        if self.player.serene:
            delta_time *= 2 / 3

        self.stopwatch += delta_time
        if self.player.dead:
            if self.stopwatch > 0.5:
                if self.player.n_continues == 0:
                    self.window.show_view(GameOver())
                else:
                    self.player.dead = False
                    self.window.show_view(ContinueMenu(self))

            return
        elif self.in_transition:
            if self.stopwatch > 2:
                self.start_stage()
        elif not (self.enemies or self.bullets or self.charms):
            self.inc_stage()
        else:
            self.stage_update(delta_time)

        self.enemies.on_update(delta_time)
        self.bullets.on_update(delta_time)
        self.friendly.on_update(delta_time)
        self.charms.on_update(delta_time)
        self.player.on_update(delta_time)

    def on_draw(self):
        self.player.draw()
        self.enemies.draw()

        # Bullet and Charm override Sprite.draw()
        # but SpriteList.draw() doesn't actually call Sprite.draw()
        for charm in self.charms:
            charm.draw()

        for friendly_bullet in self.friendly:
            friendly_bullet.draw()

        for bullet in self.bullets:
            bullet.draw()

        if self.player.blink:
            arcade.draw_rectangle_filled(
                self.player.hp_label.position[0]
                - self.player.hp_label.content_width / 2,
                self.player.hp_label.position[1]
                + self.player.hp_label.content_height / 2,
                self.player.hp_label.content_width + 20,
                self.player.hp_label.content_height + 20,
                arcade.csscolor.RED,
            )

        if self.player.serene_denied:
            arcade.draw_rectangle_filled(
                self.player.serene_label.position[0]
                + self.player.serene_label.content_width / 2,
                self.player.serene_label.position[1]
                + self.player.serene_label.content_height / 2,
                self.player.serene_label.content_width + 20,
                self.player.serene_label.content_height + 20,
                arcade.csscolor.RED,
            )

        self.player.hp_label.draw()
        self.player.score_label.draw()
        self.player.serene_label.draw()

        if self.in_transition:
            self.transition_label.draw()


class Boss(arcade.SpriteCircle):
    hp: int
    hp_label: arcade.Text


class BossStage(Stage):
    boss: Boss

    def __init__(self, previous: Stage = None):
        super().__init__(previous)

    def stage_update(self, delta_time: float):
        super().stage_update(delta_time)
        if self.boss.hp == 0:
            self.boss.hp_label.text = "Boss Vanquished!"

    def on_draw(self):
        super().on_draw()
        if not self.in_transition:
            self.boss.draw_hp_bar()
