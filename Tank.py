class Tank:

	def __init__(self, sprite, x, y, angle):
		self.sprite = sprite
		self.sprite.center_x = x
		self.sprite.center_y = y
		self.sprite.angle = angle
