import arcade
from Tank import Tank

SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 1000
SCREEN_TITLE = "Tiny Treads"


class TinyTreads(arcade.Window):
	def __init__(self):
		super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
		arcade.set_background_color(arcade.color.ALLOY_ORANGE)

		self.tank_sprite_dict = {"Tank 1" : (0,0)}

		self.all_sprites = arcade.SpriteList()
		self.tank_sprites = arcade.SpriteList()

		self.tanks = []

		self.input_stack = []

	def on_draw(self):
		arcade.start_render()
		self.tank_sprites.draw()

	def on_update(self, delta_time: float):
		self.handle_input()
		for t in self.tanks:
			t.update(delta_time)
		self.tank_sprites.on_update(delta_time)

	def handle_input(self):
		self.tanks[0].speed = 0
		self.tanks[0].br_speed = 0
		self.tanks[0].tr_speed = 0
		self.tanks[0].aim_speed = 0.0

		for symbol in self.input_stack:
			if symbol == arcade.key.W:
				self.tanks[0].speed = 50
			if symbol == arcade.key.S:
				self.tanks[0].speed = -30
			if symbol == arcade.key.A:
				self.tanks[0].br_speed = 50
			if symbol == arcade.key.D:
				self.tanks[0].br_speed = -50
			if symbol == arcade.key.Q:
				self.tanks[0].tr_speed = 50
			if symbol == arcade.key.E:
				self.tanks[0].tr_speed = -50
			if symbol == arcade.key.LSHIFT:
				self.tanks[0].turret_lock = not self.tanks[0].turret_lock
				self.tanks[0].turret_lock_sprite.alpha = (255 if self.tanks[0].turret_lock else 0)
			if symbol == arcade.key.R:
				self.tanks[0].aim_speed = 0.25
			if symbol == arcade.key.F:
				self.tanks[0].aim_speed = -0.25
			if symbol == arcade.key.SPACE:
				self.tanks[0].shoot()

	def on_key_press(self, symbol: int, modifiers: int):
		self.input_stack.append(symbol)

		"""
		if symbol == arcade.key.W:
			self.tanks[0].speed = 50
		if symbol == arcade.key.S:
			self.tanks[0].speed = -30
		if symbol == arcade.key.A:
			self.tanks[0].br_speed = 50
		if symbol == arcade.key.D:
			self.tanks[0].br_speed = -50
		if symbol == arcade.key.Q:
			self.tanks[0].tr_speed = 50
		if symbol == arcade.key.E:
			self.tanks[0].tr_speed = -50
		if symbol == arcade.key.LSHIFT:
			self.tanks[0].turret_lock = not self.tanks[0].turret_lock
			self.tanks[0].turret_lock_sprite.alpha = (255 if self.tanks[0].turret_lock else 0)
		if symbol == arcade.key.R:
			self.tanks[0].aim_speed = 0.25
		if symbol == arcade.key.F:
			self.tanks[0].aim_speed = -0.25
		if symbol == arcade.key.SPACE:
			self.tanks[0].shoot()
		"""

	def on_key_release(self, symbol: int, modifiers: int):
		self.input_stack = [s for s in self.input_stack if s != symbol]

		""""
		if symbol == arcade.key.W or symbol == arcade.key.S:
			self.tanks[0].speed = 0
		if symbol == arcade.key.A or symbol == arcade.key.D:
			self.tanks[0].br_speed = 0
		if symbol == arcade.key.Q or symbol == arcade.key.E:
			self.tanks[0].tr_speed = 0
		if symbol == arcade.key.R or symbol == arcade.key.F:
			self.tanks[0].aim_speed = 0.0
		"""

	def add_tank(self, sprite_pos, x, y, angle, max_ad):
		tank = Tank(self.tank_sprites, sprite_pos, x, y, angle, max_ad)
		self.tank_sprites.append(tank.body_sprite)
		self.tank_sprites.append(tank.turret_sprite)
		self.tank_sprites.append(tank.turret_lock_sprite)
		self.tank_sprites.append(tank.reticle_sprite)
		self.tank_sprites.append(tank.crosshair_sprite)
		self.tanks.append(tank)

	def setup(self):
		arcade.set_background_color((20, 20, 20))
		self.add_tank(self.tank_sprite_dict["Tank 1"], SCREEN_WIDTH/2, SCREEN_HEIGHT/2, 90, 500)

if __name__ == '__main__':
	app = TinyTreads()
	app.setup()
	arcade.run()
