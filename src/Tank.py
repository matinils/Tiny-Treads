import arcade
import math
from VSprite import VSprite

class Tank:

	SPRITE_SHEET_PATH = "./../res/sprite-sheet.png"

	def __init__(self, sprite_list, sprite_pos, x, y, angle, max_ad, magazine_size, rem_ammo):
		self.sprite_list = sprite_list
		self.remaining_ammo = rem_ammo
		self.magazine_size = magazine_size
		self.loaded_ammo = magazine_size
		self.reload_timer = 0

		self.speed = 0
		self.br_speed = 0
		self.tr_speed = 0
		self.max_ad = max_ad
		self.aim_distance = 0.0
		self.aim_speed = 0
		self.turret_lock = True

		self.body_sprite = VSprite(
			Tank.SPRITE_SHEET_PATH, 1.0, 
			*sprite_pos, 75, 50,
			x, y
		)
		self.body_sprite.angle = angle

		self.turret_sprite = VSprite(
			Tank.SPRITE_SHEET_PATH, 1.0,
			sprite_pos[0], sprite_pos[1] + 50, 125, 50,
			x, y
		)
		self.turret_sprite.angle = angle

		self.turret_lock_sprite = VSprite(
			Tank.SPRITE_SHEET_PATH, 1.0,
			sprite_pos[0] + 75, sprite_pos[1], 10, 14,
			x, y
		)

		self.reticle_sprite = VSprite(
			Tank.SPRITE_SHEET_PATH, 1.0,
			sprite_pos[0] + 85, sprite_pos[1], 13, 13,
			x, y + 120
		)

		self.crosshair_sprite = VSprite(
			Tank.SPRITE_SHEET_PATH, 1.0,
			sprite_pos[0] + 75, sprite_pos[1] + 14, 27, 27,
			x, y + 120
		)

		self.bullets = []
		self.bullet_sprite_pos = (sprite_pos[0] + 98, sprite_pos[1])

		self.ammo_sprites = []
		for i in range(self.loaded_ammo):
			self.ammo_sprites.append(VSprite(
				Tank.SPRITE_SHEET_PATH, 3.0,
				*self.bullet_sprite_pos, 15, 6,
				15 + i*30, 30
			))
		for ammo in self.ammo_sprites:
			ammo.angle = 90
			ammo.alpha = 0
			self.sprite_list.append(ammo)

		self.explosions = []


	def turret_tip(self):
		return (
			self.turret_sprite.center_x + 50 * math.cos(self.turret_sprite.radians),
			self.turret_sprite.center_y + 50 * math.sin(self.turret_sprite.radians)
		)

	def shoot(self):
		if self.loaded_ammo > 0 and self.reload_timer <= 0:
			self.reload_timer = 1
			self.loaded_ammo -= 1
			self.bullets.append(VSprite(
				Tank.SPRITE_SHEET_PATH, 1.0,
				*self.bullet_sprite_pos, 15, 6,
				*self.turret_tip()
			))
			self.bullets[-1].angle = self.turret_sprite.angle
			self.bullets[-1].velocity = (
				200 * math.cos(self.bullets[-1].radians),
				200 * math.sin(self.bullets[-1].radians)
			)
			self.bullets[-1].hit_x = self.reticle_sprite.center_x
			self.bullets[-1].hit_y = self.reticle_sprite.center_y
			self.bullets[-1].prev_dist = math.hypot(
				self.bullets[-1].center_x - self.bullets[-1].hit_x,
				self.bullets[-1].center_y - self.bullets[-1].hit_y
			)
			self.sprite_list.append(self.bullets[-1])

	def reload(self):
		ammo_delta = self.magazine_size - self.loaded_ammo
		if ammo_delta > 0 and self.remaining_ammo > 0:
			self.reload_timer = 5
			if ammo_delta <= self.remaining_ammo:
				self.remaining_ammo -= ammo_delta
				self.loaded_ammo = self.magazine_size
			else:
				self.loaded_ammo = self.remaining_ammo
				self.remaining_ammo = 0

	def update(self, delta_time):
		self.reload_timer -= delta_time
		for ammo in self.ammo_sprites:
			ammo.alpha = 0
		for i in range(self.loaded_ammo):
			self.ammo_sprites[-i - 1].alpha = 255

		velocity = (
			self.speed * math.cos(self.body_sprite.radians),
			self.speed * math.sin(self.body_sprite.radians)
		)
		self.body_sprite.velocity = velocity
		self.turret_sprite.velocity = velocity
		self.turret_lock_sprite.velocity = velocity
		self.body_sprite.change_angle = self.br_speed
		self.turret_sprite.change_angle = self.tr_speed + (0 if self.turret_lock else self.br_speed)

		self.aim_distance += self.aim_speed * delta_time
		self.aim_distance = max(min(self.aim_distance, 1.0), 0.0)
		aim_coord = (120 + (self.max_ad - 120) * self.aim_distance)
		aim_coord_x = aim_coord * math.cos(self.turret_sprite.radians) + self.turret_sprite.center_x
		aim_coord_y = aim_coord * math.sin(self.turret_sprite.radians) + self.turret_sprite.center_y
		self.crosshair_sprite.center_x = aim_coord_x
		self.crosshair_sprite.center_y = aim_coord_y
		self.reticle_sprite.center_x = aim_coord_x
		self.reticle_sprite.center_y = aim_coord_y

		for index, explosion in enumerate(self.explosions):
			if explosion[2] > 20:
				self.explosions.pop(index)
			else:
				explosion[2] += 5

		for index, bullet in enumerate(self.bullets):
			new_dist = math.hypot(
				bullet.center_x - bullet.hit_x,
				bullet.center_y - bullet.hit_y
			)
			if bullet.prev_dist < new_dist:
				self.bullets.pop(index)
				self.explosions.append([bullet.hit_x, bullet.hit_y, 0])
				bullet.kill()
			else:
				bullet.prev_dist = new_dist


