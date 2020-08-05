import arcade
import math
import random
import Enums
import Geometry as geom
from VSprite import VSprite

class Tank:

	SPRITE_SHEET_PATH = "./../res/sprite-sheet.png"

	def __init__(self, sprite_pos, x, y, angle, max_ad, magazine_size, rem_ammo, player_type, tank_list):
		self.sprite_list = arcade.SpriteList()
		self.remaining_ammo = rem_ammo
		self.magazine_size = magazine_size
		self.loaded_ammo = magazine_size
		self.reload_timer = 0
		self.reloading = False
		self.reload_time = 5
		self.rechamber_time = 1.0
		self.player_type = player_type
		self.tank_list = tank_list
		self.max_armor = 100
		self.max_health = 100
		self.health = self.max_health
		self.armor = self.max_armor
		self.disabled = False
		self.explosions_hit_by = []

		self.speed = 0
		self.br_speed = 0
		self.tr_speed = 0
		self.max_ad = max_ad
		self.min_ad = 120
		self.aim_distance = 0.0
		self.aim_speed = 0
		self.turret_lock = True
		self.explosion_size = 40

		self.x_target = random.randint(0,1000)
		self.y_target = random.randint(0,1000)

		self.body_sprite = VSprite(
			Tank.SPRITE_SHEET_PATH, 1.0, 
			*sprite_pos, 75, 50,
			x, y
		)
		self.body_sprite.angle = angle
		self.sprite_list.append(self.body_sprite)

		self.turret_sprite = VSprite(
			Tank.SPRITE_SHEET_PATH, 1.0,
			sprite_pos[0], sprite_pos[1] + 50, 125, 50,
			x, y
		)
		self.turret_sprite.angle = angle
		self.sprite_list.append(self.turret_sprite)

		self.turret_lock_sprite = VSprite(
			Tank.SPRITE_SHEET_PATH, 1.0,
			sprite_pos[0] + 75, sprite_pos[1], 10, 14,
			x, y
		)
		self.sprite_list.append(self.turret_lock_sprite)

		self.reticle_sprite = VSprite(
			Tank.SPRITE_SHEET_PATH, 1.0,
			sprite_pos[0] + 85, sprite_pos[1], 13, 13,
			x, y + 120
		)
		if self.player_type == Enums.PlayerType.ENEMY:
			self.reticle_sprite.alpha = 0
		self.sprite_list.append(self.reticle_sprite)

		self.crosshair_sprite = VSprite(
			Tank.SPRITE_SHEET_PATH, 1.0,
			sprite_pos[0] + 75, sprite_pos[1] + 14, 27, 27,
			x, y + 120
		)
		if self.player_type == Enums.PlayerType.ENEMY:
			self.crosshair_sprite.alpha = 0
		self.sprite_list.append(self.crosshair_sprite)

		self.bullets = []
		self.bullet_sprite_pos = (sprite_pos[0] + 98, sprite_pos[1])

		self.ammo_sprites = []
		if self.player_type == Enums.PlayerType.PLAYER1:
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
			self.reload_timer = self.rechamber_time
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
		elif self.loaded_ammo == 0 and not self.reloading:
			self.reload()

	def reload(self):
		ammo_delta = self.magazine_size - self.loaded_ammo
		if ammo_delta > 0 and self.remaining_ammo > 0:
			self.reload_timer = self.reload_time
			self.reloading = True

	def complete_reload(self):
		self.reloading = False
		ammo_delta = self.magazine_size - self.loaded_ammo
		if ammo_delta <= self.remaining_ammo:
			self.remaining_ammo -= ammo_delta
			self.loaded_ammo = self.magazine_size
		else:
			self.loaded_ammo = self.remaining_ammo
			self.remaining_ammo = 0

	def draw_to_screen(self):
		self.sprite_list.draw()
		self.body_sprite.draw_hit_box(arcade.color.RED, 5)
		for explosion in self.explosions:
			arcade.draw_circle_filled(*explosion)

		if self.player_type == Enums.PlayerType.PLAYER1:
			arcade.draw_text(f"+ {self.remaining_ammo}", 5 + self.magazine_size*30, 5, arcade.color.WHITE, 30.0)
			if self.reloading:
				arcade.draw_rectangle_outline(5 + self.magazine_size * 30 / 2, 25, self.magazine_size * 30 - 10, 30, arcade.color.WHITE)
				progress = self.magazine_size - (self.reload_timer / self.reload_time * self.magazine_size)
				pmul = (self.magazine_size * 30 - 10) / (self.magazine_size * 30)
				arcade.draw_rectangle_filled(10 + progress * 30 / 2 * pmul, 25, progress * 30 * pmul, 30, arcade.color.WHITE)

		arcade.draw_rectangle_outline(self.body_sprite.center_x, self.body_sprite.bottom - 20, 100, 20, arcade.color.GREEN)
		progress = self.health / self.max_health
		arcade.draw_rectangle_filled(self.body_sprite.center_x - 50 + 50*progress, self.body_sprite.bottom - 20, 100*progress, 20, arcade.color.GREEN)
		arcade.draw_rectangle_outline(self.body_sprite.center_x, self.body_sprite.bottom - 50, 100, 20, arcade.color.BLUE)
		progress = self.armor / self.max_armor
		arcade.draw_rectangle_filled(self.body_sprite.center_x - 50 + 50 * progress, self.body_sprite.bottom - 50, 100 * progress, 20, arcade.color.BLUE)

	def get_dist_between_angles(self, a1, a2):
		diff = abs(a1 - a2)
		return abs(diff - 360) if diff > 180 else diff

	def update(self, delta_time):
		self.reload_timer -= delta_time
		if self.player_type == Enums.PlayerType.PLAYER1:
			for ammo in self.ammo_sprites:
				ammo.alpha = 0
			for i in range(self.loaded_ammo):
				self.ammo_sprites[-i - 1].alpha = 255
		if self.reloading:
			for ammo in self.ammo_sprites:
				ammo.alpha = 0
			if self.reload_timer <= 0:
				self.complete_reload()

		for tank in self.tank_list:
			for explosion in tank.explosions:
				if explosion not in self.explosions_hit_by:
					p = self.body_sprite.points
					if self.body_sprite.collides_with_point((explosion[0], explosion[1])):
						self.explosions_hit_by.append(explosion)
						self.health -= 100 * (1 - (self.armor / self.max_armor))
						self.armor -= 50
						self.health = max(self.health, 0)
						self.armor = max(self.armor, 0)
					elif geom.circle_intersect_rectangle((explosion[0], explosion[1]), explosion[2], p[0], p[1], p[2], p[3]):
						self.explosions_hit_by.append(explosion)
						self.health -= 100 * (1 - (explosion[2] / tank.explosion_size)) * (1 - (self.armor / self.max_armor))
						explosion[3] = (255, 0, 0) + (explosion[3][3],)

		if self.health <= 0:
			self.disabled = True

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
		aim_coord = (self.min_ad + (self.max_ad - self.min_ad) * self.aim_distance)
		aim_coord_x = aim_coord * math.cos(self.turret_sprite.radians) + self.turret_sprite.center_x
		aim_coord_y = aim_coord * math.sin(self.turret_sprite.radians) + self.turret_sprite.center_y
		self.crosshair_sprite.center_x = aim_coord_x
		self.crosshair_sprite.center_y = aim_coord_y
		self.reticle_sprite.center_x = aim_coord_x
		self.reticle_sprite.center_y = aim_coord_y

		for index, explosion in enumerate(self.explosions):
			if explosion[3][3] <= 0:
				self.explosions.pop(index)
			if explosion[2] > self.explosion_size:
				explosion[3] = explosion[3][:3] + (explosion[3][3] - 1000 * delta_time,)
			else:
				explosion[2] += 80 * delta_time

		for index, bullet in enumerate(self.bullets):
			new_dist = math.hypot(
				bullet.center_x - bullet.hit_x,
				bullet.center_y - bullet.hit_y
			)
			if bullet.prev_dist < new_dist:
				self.bullets.pop(index)
				self.explosions.append([bullet.hit_x, bullet.hit_y, 0, (255,255,255,255)])
				bullet.kill()
			else:
				bullet.prev_dist = new_dist

		while self.turret_sprite.angle > 360:
			self.turret_sprite.angle -= 360
		while self.turret_sprite.angle < 0:
			self.turret_sprite.angle += 360

		if self.player_type == Enums.PlayerType.ENEMY:
			for tank in self.tank_list:
				if tank.player_type == Enums.PlayerType.PLAYER1:
					target_angle = 180 + (math.atan2(self.body_sprite.center_y - tank.body_sprite.center_y, self.body_sprite.center_x - tank.body_sprite.center_x) * 57.29)
					if self.get_dist_between_angles(target_angle, self.turret_sprite.angle) > 1:
						if self.get_dist_between_angles(target_angle, self.turret_sprite.angle + 1) < self.get_dist_between_angles(target_angle, self.turret_sprite.angle - 1):
							self.turret_sprite.angle += 50 * delta_time
						else:
							self.turret_sprite.angle -= 50 * delta_time
					target_distance = math.sqrt((self.body_sprite.center_x - tank.body_sprite.center_x)**2 + (self.body_sprite.center_y - tank.body_sprite.center_y)**2)
					reticle_distance = math.sqrt((self.body_sprite.center_x - self.reticle_sprite.center_x)**2 + (self.body_sprite.center_y - self.reticle_sprite.center_y)**2)
					if abs(target_distance - reticle_distance) > 1:
						if target_distance > reticle_distance:
							self.aim_speed = 0.25
						else:
							self.aim_speed = -0.25
					else:
						self.aim_speed = 0
					if tank.body_sprite.collides_with_point(self.reticle_sprite.position):
						self.shoot()

					travel_target_distance = math.sqrt((self.x_target - self.body_sprite.center_x)**2 + (self.y_target - self.body_sprite.center_y)**2)
					travel_target_angle = 180 + (math.atan2(self.body_sprite.center_y - self.y_target, self.body_sprite.center_x - self.x_target) * 57.29)
					if travel_target_distance < 1:
						self.speed = 0
						self.x_target = random.randint(0,1000)
						self.y_target = random.randint(0,1000)
					else:
						if self.get_dist_between_angles(travel_target_angle, self.body_sprite.angle) > 1:
							if self.get_dist_between_angles(travel_target_angle,self.body_sprite.angle + 1) < self.get_dist_between_angles(travel_target_angle, self.body_sprite.angle - 1):
								self.body_sprite.angle += 50 * delta_time
							else:
								self.body_sprite.angle -= 50 * delta_time
						else:
							self.speed = 50






		self.sprite_list.on_update(delta_time)


