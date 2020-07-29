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

		self.tank_sprite_dict = {"Tank 1" : (0,0)}

		self.all_sprites = arcade.SpriteList()
		self.tank_sprites = arcade.SpriteList()

		self.tanks = []

	def on_draw(self):
		arcade.start_render()
		self.tank_sprites.draw()

	def on_update(self, delta_time: float):
		self.tank_sprites.update()

	def on_key_press(self, symbol: int, modifiers: int):
		if symbol == arcade.key.W:
			self.tanks[0].set_velocity(1,0)

	def on_key_release(self, symbol: int, modifiers: int):
		if symbol == arcade.key.W:
			self.tanks[0].set_velocity(0,0)

	def add_tank(self, sprite_pos, x, y, angle):
		tank = Tank(sprite_pos, x, y, angle)
		self.tank_sprites.append(tank.body_sprite)
		self.tank_sprites.append(tank.turret_sprite)
		self.tanks.append(tank)

	def setup(self):
		arcade.set_background_color((17,17,17))
		self.add_tank(self.tank_sprite_dict["Tank 1"], 200, 200, 0)

if __name__ == '__main__':
	app = TinyTreads()
	app.setup()
	arcade.run()
