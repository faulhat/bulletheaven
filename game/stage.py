from abc import abstractmethod
import arcade, pyglet

from contmenu import ContinueMenu
from stopwatch import GameObject
from gameover import GameOver
from pausemenu import PauseMenu
from player import Player
from constants import *


class Stage(arcade.View, GameObject):
    MUSIC = arcade.Sound("assets/music/main.mid.mp3")
    SERENE_MUSIC = arcade.Sound("assets/music/serene.mid.mp3")
    player: pyglet.media.Player

    def __init__(self, other: "Stage" = None):
        GameObject.__init__(self)
        arcade.View.__init__(self)
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
            self.music_player = self.MUSIC.play()
            self.music_player.loop = True
            self.music_player.pause()

            self.serene_player = self.SERENE_MUSIC.play()
            self.serene_player.loop = True
            self.serene_player.pause()
        else:
            self.player = other.player
            self.enemies = other.enemies
            self.bullets = other.bullets
            self.friendly = other.friendly
            self.charms = other.charms
            self.keys = other.keys
            self.music_player = other.get_music_player()
            self.serene_player = other.serene_player

            self.player.stage = self
            self.player.exit_serene_mode()

        self.stopwatch = self.new_stopwatch()
        self.stage_stopwatch = self.new_stopwatch()
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

    def get_music_player(self):
        return self.music_player

    def play_music(self):
        if self.player.serene:
            self.music_player.pause()
            self.serene_player.play()
        elif self.music_player:
            self.serene_player.pause()
            self.music_player.play()

    @abstractmethod
    def inc_stage(self):
        pass

    @abstractmethod
    def start_stage(self):
        self.in_transition = False
        if not (self.music_player.playing or self.serene_player.playing):
            self.play_music()

    @abstractmethod
    def stage_update(self, delta_time: float):
        pass

    def on_key_press(self, symbol: int, modifiers: int):
        if symbol == arcade.key.X:
            if self.music_player:
                self.music_player.pause()

            self.serene_player.pause()
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
        self.add_all(delta_time)

        if self.player.serene:
            delta_time *= 1 / 2

        if self.player.dead:
            if self.stopwatch.check(0.5):
                if self.player.n_continues == 0:
                    self.music_player.pause()
                    self.serene_player.pause()
                    self.window.show_view(GameOver())
                else:
                    if self.music_player:
                        self.music_player.pause()
                    
                    self.serene_player.pause()
                    self.player.dead = False
                    self.window.show_view(ContinueMenu(self))

            return
        elif self.in_transition:
            if self.stopwatch.check_reset(2):
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
        elif self.player.serene:
            if self.player.serene_clock.time < 6:
                arcade.draw_rectangle_filled(
                    self.player.serene_label.position[0]
                    + self.player.serene_label.content_width / 2,
                    self.player.serene_label.position[1]
                    + self.player.serene_label.content_height / 2,
                    self.player.serene_label.content_width + 20,
                    self.player.serene_label.content_height + 20,
                    arcade.csscolor.GREEN,
                )
            else:
                arcade.draw_rectangle_filled(
                    self.player.serene_label.position[0]
                    + self.player.serene_label.content_width / 2,
                    self.player.serene_label.position[1]
                    + self.player.serene_label.content_height / 2,
                    self.player.serene_label.content_width + 20,
                    self.player.serene_label.content_height + 20,
                    arcade.csscolor.GOLDENROD,
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
    MUSIC = arcade.Sound("assets/music/boss.mid.mp3")
    boss: Boss

    def __init__(self, previous: Stage = None):
        super().__init__(previous)
        if previous:
            previous.music_player.delete()

        self.music_player = self.MUSIC.play()
        self.music_player.loop = True
        self.music_player.pause()

    def get_music_player(self):
        self.music_player.delete()
        self.music_player = Stage.MUSIC.play()
        self.music_player.loop = True
        self.music_player.pause()
        return self.music_player

    def stage_update(self, delta_time: float):
        super().stage_update(delta_time)
        if self.boss.hp == 0:
            self.boss.hp_label.text = "Boss Vanquished!"

    def on_draw(self):
        super().on_draw()
        if not self.in_transition:
            self.boss.draw_hp_bar()
