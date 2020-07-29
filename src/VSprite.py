import arcade

class VSprite(arcade.Sprite):
	def on_update(self, delta_time: float = 1/60):
		self.position = [self._position[0] + self.change_x * delta_time, self._position[1] + self.change_y * delta_time]
		self.angle += self.change_angle * delta_time