import arcade
import math

class Tank:

	SPRITE_SHEET_PATH = "./../res/sprite-sheet.png"

	def __init__(self, sprite_pos, x, y, angle, max_ad):
		self.speed = 0
		self.br_speed = 0
		self.tr_speed = 0
		self.max_ad = max_ad
		self.aim_distance = 0.0
		self.aim_speed = 0
		self.turret_lock = True

		self.body_sprite = arcade.Sprite(
			Tank.SPRITE_SHEET_PATH, 1.0, 
			*sprite_pos, 75, 50,
			x, y
		)
		self.body_sprite.angle = angle

		self.turret_sprite = arcade.Sprite(
			Tank.SPRITE_SHEET_PATH, 1.0,
			sprite_pos[0], sprite_pos[1] + 50, 125, 50,
			x, y
		)
		self.turret_sprite.angle = angle

		self.turret_lock_sprite = arcade.Sprite(
			Tank.SPRITE_SHEET_PATH, 1.0,
			sprite_pos[0] + 75, sprite_pos[1], 10, 14,
			x, y
		)

		self.reticle_sprite = arcade.Sprite(
			Tank.SPRITE_SHEET_PATH, 1.0,
			sprite_pos[0] + 85, sprite_pos[1], 13, 13,
			x, y + 120
		)

		self.crosshair_sprite = arcade.Sprite(
			Tank.SPRITE_SHEET_PATH, 1.0,
			sprite_pos[0] + 75, sprite_pos[1] + 14, 27, 27,
			x, y + 120
		)

	def update(self):
		velocity = (
			self.speed * math.cos(self.body_sprite.radians),
			self.speed * math.sin(self.body_sprite.radians))
		self.body_sprite.velocity = velocity
		self.turret_sprite.velocity = velocity
		self.turret_lock_sprite.velocity = velocity
		self.body_sprite.change_angle = self.br_speed
		self.turret_sprite.change_angle = self.tr_speed + (0 if self.turret_lock else self.br_speed)

		self.aim_distance += self.aim_speed
		self.aim_distance = max(min(self.aim_distance, 1.0), 0.0)
		aim_coord = (120 + (self.max_ad - 120) * self.aim_distance)
		aim_coord_x = aim_coord * math.cos(self.turret_sprite.radians) + self.turret_sprite.center_x
		aim_coord_y = aim_coord * math.sin(self.turret_sprite.radians) + self.turret_sprite.center_y
		self.crosshair_sprite.center_x = aim_coord_x
		self.crosshair_sprite.center_y = aim_coord_y
		self.reticle_sprite.center_x = aim_coord_x
		self.reticle_sprite.center_y = aim_coord_y