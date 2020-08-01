import arcade
from Tank import Tank
import Enums

SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 1000
SCREEN_TITLE = "Tiny Treads"


class TinyTreads(arcade.Window):
	def __init__(self):
		super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
		arcade.set_background_color(arcade.color.ALLOY_ORANGE)
		self.tank_sprite_dict = {"Tank 1" : (0,0)}
		self.tanks = []
		self.player1_tank = None
		self.input_stack = []

	def on_draw(self):
		arcade.start_render()
		for t in self.tanks:
			t.draw_to_screen()

	def on_update(self, delta_time: float):
		self.handle_input()
		for t in self.tanks:
			t.update(delta_time)

	def handle_input(self):
		self.player1_tank.speed = 0
		self.player1_tank.br_speed = 0
		self.player1_tank.tr_speed = 0
		self.player1_tank.aim_speed = 0.0
		for symbol in self.input_stack:
			if symbol == arcade.key.W:
				self.player1_tank.speed = 50
			if symbol == arcade.key.S:
				self.player1_tank.speed = -30
			if symbol == arcade.key.A:
				self.player1_tank.br_speed = 50
			if symbol == arcade.key.D:
				self.player1_tank.br_speed = -50
			if symbol == arcade.key.Q:
				self.player1_tank.tr_speed = 50
			if symbol == arcade.key.E:
				self.player1_tank.tr_speed = -50
			if symbol == arcade.key.R:
				self.player1_tank.aim_speed = 0.25
			if symbol == arcade.key.F:
				self.player1_tank.aim_speed = -0.25

	def on_key_press(self, symbol: int, modifiers: int):
		self.input_stack.append(symbol)
		if symbol == arcade.key.SPACE:
			self.player1_tank.shoot()
		if symbol == arcade.key.C:
			self.player1_tank.reload()
		if symbol == arcade.key.LSHIFT:
			self.player1_tank.turret_lock = not self.player1_tank.turret_lock
			self.player1_tank.turret_lock_sprite.alpha = (255 if self.player1_tank.turret_lock else 0)

	def on_key_release(self, symbol: int, modifiers: int):
		self.input_stack = [s for s in self.input_stack if s != symbol]

	def add_tank(self, sprite_pos, x, y, angle, max_ad, mag_size, start_ammo, player_type):
		tank = Tank(sprite_pos, x, y, angle, max_ad, mag_size, start_ammo, player_type, self.tanks)
		if player_type == Enums.PlayerType.PLAYER1:
			self.player1_tank = tank
		self.tanks.append(tank)

	def setup(self):
		arcade.set_background_color((20, 20, 20))
		self.add_tank(self.tank_sprite_dict["Tank 1"], SCREEN_WIDTH/2, SCREEN_HEIGHT/2, 90, 500, 5, 10, Enums.PlayerType.PLAYER1)
		self.add_tank(self.tank_sprite_dict["Tank 1"], SCREEN_WIDTH / 4, SCREEN_HEIGHT / 4, 0, 500, 5, 10,
					  Enums.PlayerType.ENEMY)


if __name__ == '__main__':
	app = TinyTreads()
	app.setup()
	arcade.run()
