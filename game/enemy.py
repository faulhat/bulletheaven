from abc import abstractproperty
from random import random
import arcade

from constants import *
from charm import Charm


class Stage(arcade.View):
    enemies: arcade.SpriteList


class Enemy(arcade.SpriteCircle):
    COLOR: arcade.Color

    def __init__(
        self,
        radius: int,
        x: float,
        y: float,
        stage: Stage,
        init_hp: int,
        drop_chance: float = 0.2,
    ):
        super().__init__(radius, self.COLOR)
        self.normal_texture = self.texture
        self.on_hit_texture = arcade.make_circle_texture(
            radius * 2, arcade.csscolor.RED
        )

        self.set_position(x, y)
        stage.enemies.append(self)
        self.stage = stage
        self.hp = init_hp
        self.hit = False
        self.hit_wait_clock = 0
        self.hit_counter = 0
        self.drop_chance = drop_chance

    def on_hit(self):
        self.hit_wait_clock = 0
        self.hit = True
        self.texture = self.on_hit_texture

    def on_update(self, delta_time: float):
        self.hit_wait_clock += delta_time
        if self.hit:
            if self.hit_wait_clock > 0.1:
                self.hit = False
                self.texture = self.normal_texture
        
        hits = self.collides_with_list(self.stage.friendly)
        if hits:
            self.hp -= 1
            if self.hp == 0:
                self.on_die()
            else:
                self.on_hit()

            for player_bullet in hits:
                player_bullet.remove_from_sprite_lists()

    def on_die(self):
        self.remove_from_sprite_lists()
        self.stage.player.inc_score()

        if random() < self.drop_chance:
            Charm(self.position[0], self.position[1], self.stage)


class Boss:
    HP_BAR_HEIGHT = 30
    BOSS_INIT_HP: int
    NAME: str

    hp: int
    hp_label: arcade.Text

    def __init__(self):
        self.hp = self.BOSS_INIT_HP
        self.hp_label = arcade.Text(
            f"{self.NAME}'s HP: {self.BOSS_INIT_HP}",
            20,
            HEIGHT - self.HP_BAR_HEIGHT / 2,
            arcade.csscolor.RED,
            font_size=18,
            font_name="PressStart2P",
            anchor_y="center",
        )

    def draw_hp_bar(self):
        arcade.draw_rectangle_filled(
            self.hp / self.BOSS_INIT_HP * WIDTH / 2,
            HEIGHT - Boss.HP_BAR_HEIGHT / 2,
            self.hp / self.BOSS_INIT_HP * WIDTH,
            Boss.HP_BAR_HEIGHT,
            arcade.csscolor.GREEN,
        )

        self.hp_label.draw()

    def update_hp_bar(self):
        self.hp_label.text = f"{self.NAME}'s HP: {self.hp}"
