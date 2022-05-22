import math
import arcade


class Stage(arcade.View):
    def __init__(self):
        super().__init__()
        self.player = arcade.SpriteCircle(15, arcade.csscolor.ALICE_BLUE)
        self.player.set_position(self.window.width / 2, self.window.height / 3)

        self.player_speed = 500
        self.enemies = arcade.SpriteList()
        self.bullets = arcade.SpriteList()
        self.keys = set()

    def on_key_press(self, symbol: int, modifiers: int):
        self.keys.add(symbol)
        return super().on_key_press(symbol, modifiers)

    def on_key_release(self, _symbol: int, _modifiers: int):
        self.keys.discard(_symbol)
        return super().on_key_release(_symbol, _modifiers)

    def on_update(self, delta_time: float):
        for enemy in self.enemies:
            enemy.on_update(delta_time)
        
        for bullet in self.bullets:
            bullet.on_update(delta_time)

        true_player_speed = self.player_speed
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

    def on_draw(self):
        self.player.draw()
        self.enemies.draw()
        self.bullets.draw()
