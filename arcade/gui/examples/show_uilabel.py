import arcade

import arcade.gui
from arcade.gui import UIManager


class MyView(arcade.View):
    def __init__(self, window: arcade.Window):
        super().__init__()

        self.window = window
        self.ui_manager = UIManager(window)

    def on_draw(self):
        arcade.start_render()
        arcade.set_background_color(arcade.color.BLACK)

    def on_show_view(self):
        print('on_show_view')
        self.setup()

    def setup(self):
        self.ui_manager.purge_ui_elements()

        self.ui_manager.add_ui_element(arcade.gui.UILabel(
            text='Hello world',
            center_x=self.window.width // 2,
            center_y=self.window.height // 2,
        ))


if __name__ == '__main__':
    window = arcade.Window(title='ARCADE_GUI')
    window.show_view(MyView(window))
    arcade.run()
