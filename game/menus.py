import arcade
from typing import Callable


class MenuItem:
    def __init__(self, text: str, does: Callable[[arcade.View], None], *args, **kwargs):
        self.text = text
        self.label = arcade.Text(f"  {self.text}", *args, **kwargs)
        self.selected = False
        self.does = does

    def select(self):
        if not self.selected:
            self.label.text = f"> {self.text}"
            self.selected = True

    def deselect(self):
        if self.selected:
            self.label.text = f"  {self.text}"
            self.selected = False


class MenuItems:
    def __init__(self, items: list[MenuItem], selected: int = 0):
        self.items = items
        self.selected = selected
        for i, item in enumerate(self.items):
            if i == self.selected:
                item.select()
            else:
                item.deselect()

    def select(self, i: int):
        self.items[self.selected].deselect()
        self.selected = i
        self.items[self.selected].select()

    def decrement(self):
        if self.selected > 0:
            self.select(self.selected - 1)

    def increment(self):
        if self.selected < len(self.items) - 1:
            self.select(self.selected + 1)

    def get(self) -> MenuItem:
        return self.items[self.selected]


class Menu(arcade.View):
    options: MenuItems

    def on_key_press(self, symbol: int, modifiers: int):
        if symbol == arcade.key.UP:
            self.options.decrement()

        if symbol == arcade.key.DOWN:
            self.options.increment()

        if symbol == arcade.key.ENTER:
            self.options.get().does(self)

        return super().on_key_press(symbol, modifiers)

    def on_draw(self):
        for option in self.options.items:
            option.label.draw()
