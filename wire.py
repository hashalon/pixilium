#!/usr/bin/python


# represent a wire that can be activated by logic gates
class Wire:
	
	def __init__ (self):
		self.active     = False
		self.was_active = False
		self.draw_off = []
		self.draw_on  = []
	
	# assign the sprites to this wire
	def add_sprite (self, position, sprite_off, sprite_on):
		self.draw_off.append((sprite_off, position))
		self.draw_on .append((sprite_on , position))
		return self
	
	# merge two wires together
	def merge (self, other):
		if self != other:
			self.draw_off += other.draw_off
			self.draw_on  += other.draw_on
		return self
	
	# reset the activation of the wire for next frame
	def update (self):
		self.was_active = self.active
		self.active     = False
	
	# try to activate the wire
	def activate (self, value):
		self.active |= value
	
	# draw the wire on the screen
	def draw (self, screen):
		screen.blits(self.draw_on if self.active else self.draw_off)

