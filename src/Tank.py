import arcade
import math

class Tank:

	SPRITE_SHEET_PATH = "./../res/sprite-sheet.png"

	def __init__(self, sprite_pos, x, y, angle):
		# self.body_angle = angle
		# self.turret_angle = 0
		self.speed = 0
		self.br_speed = 0

		self.body_sprite = arcade.Sprite(
			Tank.SPRITE_SHEET_PATH, 1.0, 
			*sprite_pos, 75, 50,
			x, y)
		self.body_sprite.angle = angle

		self.turret_sprite = arcade.Sprite(
			Tank.SPRITE_SHEET_PATH, 1.0,
			sprite_pos[0], sprite_pos[1] + 50, 125, 50,
			x, y)
		self.turret_sprite.angle = angle

	def update(self):
		velocity = (
			self.speed * math.cos(self.body_sprite.radians),
			self.speed * math.sin(self.body_sprite.radians))
		self.body_sprite.velocity = velocity
		self.turret_sprite.velocity = velocity
		self.body_sprite.change_angle = self.br_speed