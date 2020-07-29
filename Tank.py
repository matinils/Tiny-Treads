import arcade

class Tank:

	SPRITE_SHEET_PATH = "./res/sprite-sheet.png"

	def __init__(self, sprite_pos, x, y, angle):
		self.body_sprite = arcade.Sprite(
			Tank.SPRITE_SHEET_PATH, 1.0, 
			*sprite_pos, 50, 75,
			x, y)
		self.body_sprite.angle = angle

		self.turret_sprite = arcade.Sprite(
			Tank.SPRITE_SHEET_PATH, 1.0,
			sprite_pos[0] + 50, sprite_pos[1], 50, 125,
			x, y)
		self.turret_angle = 0
		self.turret_sprite.angle = angle
