from abc import abstractmethod
import math
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

            self.keys = set()
        else:
            self.player = other.player
            self.enemies = other.enemies
            self.bullets = other.bullets
            self.friendly = other.friendly
            self.keys = other.keys

        self.stopwatch = 0
        self.stage_stopwatch = 0
        self.transition_label = arcade.Text(
            f"",
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

        self.keys.add(symbol)
        return super().on_key_press(symbol, modifiers)

    def on_key_release(self, _symbol: int, _modifiers: int):
        self.keys.discard(_symbol)
        return super().on_key_release(_symbol, _modifiers)

    def on_update(self, delta_time: float):
        self.stopwatch += delta_time
        self.player.firing_stopwatch += delta_time

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
        elif len(self.enemies) == 0 and len(self.bullets) == 0:
            self.inc_stage()
        else:
            self.stage_update(delta_time)

        self.enemies.on_update(delta_time)
        self.bullets.on_update(delta_time)
        self.friendly.on_update(delta_time)

        true_player_speed = Player.SPEED
        if arcade.key.S in self.keys:
            self.slow = True
            true_player_speed /= 2
        else:
            self.slow = False

        offset = true_player_speed * delta_time
        diag_offset = offset * 1 / math.sqrt(2)
        x, y = self.player.position
        if arcade.key.UP in self.keys and arcade.key.DOWN not in self.keys:
            if arcade.key.LEFT in self.keys and arcade.key.RIGHT not in self.keys:
                x -= diag_offset
                y += diag_offset
            elif arcade.key.RIGHT in self.keys and arcade.key.LEFT not in self.keys:
                x += diag_offset
                y += diag_offset
            else:
                y += offset
        elif arcade.key.DOWN in self.keys and arcade.key.UP not in self.keys:
            if arcade.key.LEFT in self.keys and arcade.key.RIGHT not in self.keys:
                x -= diag_offset
                y -= diag_offset
            elif arcade.key.RIGHT in self.keys and arcade.key.LEFT not in self.keys:
                x += diag_offset
                y -= diag_offset
            else:
                y -= offset
        elif arcade.key.LEFT in self.keys and arcade.key.RIGHT not in self.keys:
            x -= offset
        elif arcade.key.RIGHT in self.keys and arcade.key.LEFT not in self.keys:
            x += offset

        self.player.set_position(x, y)

        if self.player.invincible:
            # Make player sprite blink while invincible
            blink_clock = int(self.stopwatch * 5) % 2
            if blink_clock == 0:
                self.player.blink = True
                self.player.texture = self.player.on_hit_texture
                self.player.hp_label.color = arcade.csscolor.BLACK

            if blink_clock == 1:
                self.player.blink = False
                self.player.texture = self.player.normal_texture
                self.player.hp_label.color = arcade.csscolor.WHITE

            if self.stopwatch > 2:
                self.player.blink = False
                self.player.invincible = False
                self.player.texture = self.player.normal_texture
                self.player.hp_label.color = arcade.csscolor.WHITE

        # The player fires a steady stream of bullets
        if self.player.firing_stopwatch > 0.1:
            Player.FriendlyBullet(
                self.player.position[0],
                self.player.position[1] + 20,
                self,
            )
            self.player.firing_stopwatch = 0

        enemy_hits = self.player.collides_with_list(self.bullets)
        if not self.player.invincible and (
            enemy_hits or self.player.collides_with_list(self.enemies)
        ):
            self.player.set_hp(self.player.hp - 1)
            if self.player.hp == 0:
                # The player is dead
                self.player.dead = True
                self.player.texture = self.player.on_hit_texture
                self.stopwatch = 0

            for bullet in enemy_hits:
                bullet.remove_from_sprite_lists()

            self.player.invincible = True
            self.stopwatch = 0

        for enemy in self.enemies:
            hits = enemy.collides_with_list(self.friendly)
            if hits:
                enemy.hp -= 1
                if enemy.hp == 0:
                    enemy.on_die()
                else:
                    enemy.on_hit()

                for friendly_bullet in hits:
                    friendly_bullet.remove_from_sprite_lists()

    def on_draw(self):
        self.player.draw()
        self.enemies.draw()
        self.bullets.draw()
        self.friendly.draw()

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

        self.player.hp_label.draw()
        self.player.score_label.draw()

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
