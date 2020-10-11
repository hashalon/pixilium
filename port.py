#!/usr/bin/python


import itertools


class Port:
	
	def __init__ (self, outputs=[], position=(0,0), sprite_off=None, sprite_on=None):
		self.active     = False
		self.outputs    = outputs
		self.position   = position
		self.sprite_off = sprite_off
		self.sprite_on  = sprite_on
		
	# update the values on each individual output wire
	def update (self, values=[]):
		self.active = True in values
		for output, value in itertools.zip_longest(self.outputs, values, fillvalue=False):
			if output: output.activate(value)
	
	
	# draw the logic gate on the screen
	def draw (self, screen):
		spr = self.sprite_on if self.active else self.sprite_off
		if spr: screen.blit(spr, self.position)
	
	
	# draw the background of the wire once
	def draw_background (self, background):
		background.blit(self.sprite_off, self.position)
	
	# draw the foreground if necessary
	def draw_foreground (self, screen):
		if self.active: screen.blit(self.sprite_on, self.position)
