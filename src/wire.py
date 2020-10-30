#!/usr/bin/python


# represent a wire that can be activated by logic gates
class Wire:
	
	def __init__ (self):
		self.active     = False
		self.was_active = False
		self.stamps_off = []
		self.stamps_on  = []
	
	
	# assign the sprites to this wire
	def add_stamp (self, position, stamp_off, stamp_on):
		self.stamps_off.append((stamp_off, position))
		self.stamps_on .append((stamp_on , position))
		return self
	
	
	# merge two wires together
	def merge (self, other):
		if self != other:
			self.stamps_off += other.stamps_off
			self.stamps_on  += other.stamps_on
		return self
	
	
	# reset the activation of the wire for next frame
	def update (self):
		self.was_active = self.active
		self.active     = False
	
	
	# try to activate the wire
	def activate (self, value):
		self.active |= value
	
	
	# draw the background of the wire once
	def draw_background (self, background):
		background.blits(self.stamps_off)
		self.stamps_off = None # release
	
	
	# draw the foreground if necessary
	def draw (self, screen):
		if self.active: screen.blits(self.stamps_on)

