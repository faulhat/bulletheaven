import math
import arcade

from bullets import Bullet
from youwin import YouWin
from gameover import GameOver


class Player(arcade.SpriteCircle):
    class FriendlyBullet(Bullet):
        def __init__(self, x, y):
            super().__init__(6, (65, 105, 255, 240), x, y, math.pi * 1/2, 600)

    def __init__(self, init_x, init_y, hp_label_x, hp_label_y):
        super().__init__(15, arcade.csscolor.ALICE_BLUE)
        self.hp = 5
        self.invincible = False
        self.speed = 500
        self.init_x = init_x
        self.init_y = init_y
        self.set_position(init_x, init_y)
        self.hp_label = arcade.Text(
            "HP: 5", hp_label_x, hp_label_y, anchor_x="right", font_name="PressStart2P"
        )
        self.dead = False
        self.won = False
        self.firing_stopwatch = 0

    def set_hp(self, hp: int):
        self.hp = hp
        self.hp_label.text = f"HP: {hp}"


class Stage(arcade.View):
    def __init__(self):
        super().__init__()
        self.player = Player(
            self.window.width / 2,
            self.window.height / 3,
            self.window.width - 20,
            self.window.height - 30,
        )

        self.enemies = arcade.SpriteList()

        # Sprite list for enemy bullets
        self.bullets = arcade.SpriteList()

        # Sprite list for the player's bullets
        self.friendly = arcade.SpriteList()

        self.keys = set()
        self.stopwatch = 0

    def on_key_press(self, symbol: int, modifiers: int):
        self.keys.add(symbol)
        return super().on_key_press(symbol, modifiers)

    def on_key_release(self, _symbol: int, _modifiers: int):
        self.keys.discard(_symbol)
        return super().on_key_release(_symbol, _modifiers)

    def on_update(self, delta_time: float):
        self.stopwatch += delta_time
        self.player.firing_stopwatch += delta_time

        if self.player.dead:
            if self.stopwatch > 1:
                self.window.show_view(GameOver())

            return
        elif self.player.won:
            if self.stopwatch > 1:
                self.window.show_view(YouWin())

        self.enemies.on_update(delta_time)
        self.bullets.on_update(delta_time)
        self.friendly.on_update(delta_time)

        true_player_speed = self.player.speed
        if arcade.key.MOD_SHIFT in self.keys:
            true_player_speed /= 2

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

        x = min(self.window.width, max(0, x))
        y = min(self.window.height, max(0, y))
        self.player.set_position(x, y)

        if self.player.invincible:
            # Make player sprite blink while invincible
            blink_clock = int(self.stopwatch * 5) % 2
            if blink_clock == 0:
                self.player.color = arcade.csscolor.ORANGE
            if blink_clock == 1:
                self.player.color = arcade.csscolor.ALICE_BLUE

            if self.stopwatch > 3:
                self.player.invincible = False
                self.player.color = arcade.csscolor.ALICE_BLUE
        else:
            # The player fires a steady stream of bullets when not invincible
            if self.player.firing_stopwatch > 0.1:
                self.friendly.append(Player.FriendlyBullet(self.player.position[0], self.player.position[1] + 20))
                self.player.firing_stopwatch = 0

        if not self.player.invincible and (self.player.collides_with_list(self.bullets) or self.player.collides_with_list(self.enemies)):
            if self.player.hp - 1 == 0:
                # The player is dead
                self.player.dead = True
                self.player.color = arcade.csscolor.PALE_VIOLET_RED
                self.stopwatch = 0

            self.bullets.clear()
            self.player.set_hp(self.player.hp - 1)
            self.player.set_position(self.player.init_x, self.player.init_y)
            self.player.invincible = True
            self.stopwatch = 0
        
        for enemy in self.enemies:
            if enemy.collides_with_list(self.friendly):
                if enemy.hp - 1 == 0:
                    enemy.remove_from_sprite_lists()
                    if len(self.enemies) == 0:
                        self.bullets.clear()
                        self.player.won = True
                        self.stopwatch = 0
                else:
                    enemy.hp -= 1

    def on_draw(self):
        self.player.draw()
        self.enemies.draw()
        self.bullets.draw()
        self.friendly.draw()
        self.player.hp_label.draw()
