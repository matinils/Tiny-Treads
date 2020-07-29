import arcade
from Tank import Tank

SCREEN_WIDTH = 600
SCREEN_HEIGHT = 800
SCREEN_TITLE = "Test Window"
RADIUS = 150


class TinyTreads(arcade.Window):
	def __init__(self):
		super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
		arcade.set_background_color(arcade.color.ALLOY_ORANGE)

		self.all_sprites = arcade.SpriteList()
		self.tank_sprites = arcade.SpriteList()

	def on_draw(self):
		arcade.start_render()
		arcade.draw_circle_filled(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2, RADIUS, arcade.color.BLUE)
		self.tank_sprites.draw()

	def add_tank(self, x, y, angle):
		tank_sprite = arcade.Sprite("res/sprite-sheet.png", 1.0)
		tank = Tank(tank_sprite, x, y, angle)
		self.tank_sprites.append(tank.sprite)

	def setup(self):
		arcade.set_background_color((17,17,17))
		self.add_tank(200, 200, 0)


if __name__ == '__main__':
	app = TinyTreads()
	app.setup()
	arcade.run()
	print("Test")
