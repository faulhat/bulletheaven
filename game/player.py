import math
import arcade

from bullets import Bullet
from constants import *


class Stage(arcade.View):
    keys: set
    enemies: arcade.SpriteList
    bullets: arcade.SpriteList
    charms: arcade.SpriteList


class FriendlyBullet(Bullet):
    def __init__(self, x: float, y: float, stage: arcade.View):
        super().__init__(
            arcade.csscolor.BLUE, x, y, math.pi * 1 / 2, 600, stage, friendly=True
        )


class Player(arcade.SpriteCircle):
    RADIUS = 15
    SPEED = 400
    INIT_HP = 10

    def __init__(self, init_x: float, init_y: float, stage: arcade.View):
        super().__init__(Player.RADIUS, arcade.csscolor.WHITE)
        self.normal_texture = self.texture
        self.on_hit_texture = arcade.make_circle_texture(
            Player.RADIUS * 2, arcade.csscolor.RED
        )

        self.stage = stage
        self.set_position(init_x, init_y)

        self.hp = Player.INIT_HP
        self.invincible = False
        self.hp_label = arcade.Text(
            f"HP: {self.hp}",
            WIDTH - 30,
            HEIGHT - 70,
            anchor_x="right",
            font_name="PressStart2P",
            font_size=18,
        )

        self.score = 0
        self.score_label = arcade.Text(
            f"SCORE: {self.score}",
            30,
            HEIGHT - 70,
            font_name="PressStart2P",
            font_size=18,
        )

        self.n_charms = 2
        self.serene_label = arcade.Text(
            f"CHARMS: {self.n_charms}",
            30,
            30,
            anchor_y="bottom",
            font_name="PressStart2P",
            font_size=18,
        )

        self.dead = False
        self.slow = False
        self.fire_clock = 0
        self.serene_clock = 0
        self.blinker_clock = 0
        self.blinker_counter = 0
        self.blink = False

        self.n_continues = 2
        self.serene = False
        self.serene_denied = False

    def set_score(self, score: int):
        self.score = score
        self.score_label.text = f"SCORE: {self.score}"

    def set_hp(self, hp: int):
        self.hp = hp
        self.hp_label.text = f"HP: {hp}"

    def inc_score(self, n: int = 1):
        for _ in range(n):
            self.score += 1
            if self.score % 5 == 0:
                self.set_hp(self.hp + 1)

        self.score_label.text = f"SCORE: {self.score}"

    def inc_charms(self, n: int = 1):
        self.n_charms += n
        if not self.serene:
            self.serene_label.text = f"CHARMS: {self.n_charms}"

        if self.serene_denied:
            self.exit_serene_denied()

    def use_charm(self):
        if not self.serene:
            if self.n_charms:
                self.serene = True
                self.serene_denied = False
                self.n_charms -= 1
                self.serene_label.text = "SERENITY MODE"
                self.serene_clock = 0
            else:
                self.serene_denied = True
                self.serene_label.text = "NO CHARMS!"
                self.serene_label.color = arcade.csscolor.BLACK
                self.serene_clock = 0

    def exit_serene_mode(self):
        if self.serene:
            self.serene = False
            self.serene_label.text = f"CHARMS: {self.n_charms}"

    def exit_serene_denied(self):
        if self.serene_denied:
            self.serene_denied = False
            self.serene_label.text = f"CHARMS: {self.n_charms}"
            self.serene_label.color = arcade.csscolor.WHITE

    def set_position(self, x: float, y: float):
        x = min(
            WIDTH - self.width / 2,
            max(self.width / 2, x),
        )
        y = min(
            HEIGHT - self.width / 2,
            max(self.width / 2, y),
        )
        super().set_position(x, y)

    def toggle_blinker(self):
        if not self.blink:
            self.blink = True
            self.texture = self.on_hit_texture
            self.hp_label.color = arcade.csscolor.BLACK
        else:
            self.blink = False
            self.texture = self.normal_texture
            self.hp_label.color = arcade.csscolor.WHITE

    def on_update(self, delta_time: float):
        self.fire_clock += delta_time
        self.serene_clock += delta_time
        self.blinker_clock += delta_time

        true_speed = Player.SPEED
        if arcade.key.Z in self.stage.keys:
            self.slow = True
            true_speed /= 2
        else:
            self.slow = False

        offset = true_speed * delta_time
        diag_offset = offset * 1 / math.sqrt(2)
        x, y = self.position

        goUp = arcade.key.UP in self.stage.keys or arcade.key.W in self.stage.keys
        goDown = arcade.key.DOWN in self.stage.keys or arcade.key.S in self.stage.keys
        goRight = arcade.key.RIGHT in self.stage.keys or arcade.key.D in self.stage.keys
        goLeft = arcade.key.LEFT in self.stage.keys or arcade.key.A in self.stage.keys
        if goUp and not goDown:
            if goLeft and not goRight:
                x -= diag_offset
                y += diag_offset
            elif goRight and not goLeft:
                x += diag_offset
                y += diag_offset
            else:
                y += offset
        elif goDown and not goUp:
            if goLeft and not goRight:
                x -= diag_offset
                y -= diag_offset
            elif goRight and not goLeft:
                x += diag_offset
                y -= diag_offset
            else:
                y -= offset
        elif goLeft and not goRight:
            x -= offset
        elif goRight and not goLeft:
            x += offset

        self.set_position(x, y)

        if self.invincible:
            # Make player sprite blink while invincible
            if self.blinker_clock > 0.2:
                self.blinker_clock = 0
                self.blinker_counter += 1
                if self.blinker_counter > 10:
                    self.blinker_counter = 0
                    self.blink = False
                    self.invincible = False
                    self.texture = self.normal_texture
                    self.hp_label.color = arcade.csscolor.WHITE
                else:
                    self.toggle_blinker()
        else:
            enemy_hits = self.collides_with_list(self.stage.bullets)
            if enemy_hits or self.collides_with_list(self.stage.enemies):
                self.set_hp(self.hp - 1)
                if self.hp == 0:
                    # The player is dead
                    self.dead = True
                    self.texture = self.on_hit_texture

                for bullet in enemy_hits:
                    bullet.remove_from_sprite_lists()

                self.invincible = True
                self.blinker_clock = 0

        charms_caught = self.collides_with_list(self.stage.charms)
        for charm in charms_caught:
            charm.remove_from_sprite_lists()
            self.inc_charms()

        # The player fires a steady stream of bullets
        if self.fire_clock > 0.1:
            FriendlyBullet(
                self.position[0],
                self.position[1] + 20,
                self.stage,
            )
            self.fire_clock = 0

        if self.serene_clock > 7 and self.serene:
            self.exit_serene_mode()
        elif self.serene_clock > 1 and self.serene_denied:
            self.exit_serene_denied()
