import arcade
import math

class Tank:

	SPRITE_SHEET_PATH = "./../res/sprite-sheet.png"

	def __init__(self, sprite_pos, x, y, angle):
		self.body_angle = angle
		self.turret_angle = 0

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

	def set_speed(self, s):
		velocity = (
			s * math.cos(math.radians(self.body_angle)),
			s * math.sin(math.radians(self.body_angle)))
		self.body_sprite.velocity = velocity
		self.turret_sprite.velocity = velocity
