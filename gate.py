#!/usr/bin/python


from const import *


class Gate:
	
	# generate a new logic gate
	def __init__ (self, gtype, position=(0,0), sprite_off=None, sprite_on=None):
		self.active     = False
		self.gtype      = gtype
		self.inputs     = []
		self.outputs    = []
		self.position   = position
		self.sprite_off = sprite_off
		self.sprite_on  = sprite_on
		self.operation  = GATE_FUNCTIONS[self.gtype]
		
	
	# add a wire as an input of this gate
	def add_input (self, inpt):
		if not inpt in self.inputs and not inpt in self.outputs:
			self.inputs.append(inpt)
	
	# add a wire as an output of this gate
	def add_output (self, outpt):
		if not outpt in self.outputs and not outpt in self.inputs:
			self.outputs.append(outpt)
	
	# update the state of the logic gate and connected wires
	def update (self):
		values = [inpt.was_active for inpt in self.inputs]
		self.active = self.operation(values)
		for outpt in self.outputs:
			outpt.activate(self.active)
	
	
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



