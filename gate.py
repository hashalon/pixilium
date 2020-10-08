#!/usr/bin/python


from const import *


class Gate:
	
	# generate a new logic gate
	def __init__ (self, gtype, position=(0,0), sprite_off=None, sprite_on=None):
		self.gtype      = gtype
		self.inputs     = []
		self.outputs    = []
		self.active     = False
		self.position   = position
		self.sprite_off = sprite_off
		self.sprite_on  = sprite_on
		
		if   gtype == GATE_AND : self.operation = gate_and
		elif gtype == GATE_XOR : self.operation = gate_xor
		elif gtype == GATE_NAND: self.operation = gate_nand
		elif gtype == GATE_XNOR: self.operation = gate_xnor
		elif gtype == GATE_NOR or gtype == GATE_NOT: self.operation = gate_nor
		else: self.operation = gate_or
	
	# add a wire as an input of this gate
	def add_input (self, inpt):
		if not inpt in self.inputs:
			self.inputs.append(inpt)
	
	# add a wire as an output of this gate
	def add_output (self, outpt):
		if not outpt in self.outputs:
			self.outputs.append(outpt)
	
	# return true if the gate has at least one input and one output
	def is_connected (self):
		return self.inputs and self.outputs
	
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
		self.sprite_off = None # garbage collect
	
	# draw the foreground if necessary
	def draw_foreground (self, screen):
		if self.active: screen.blit(self.sprite_on, self.position)
		

# boolean operations
def gate_nand (values): return not gate_and(values)
def gate_nor  (values): return not gate_or (values)
def gate_xnor (values): return not gate_xor(values)
def gate_and  (values): return not (False in values)
def gate_or   (values): return True in values
def gate_xor  (values): return values.count(True) == len(values) / 2


if __name__ == "__main__":
	off = [False, False, False, False]
	mid = [False, True , False, True ]
	on  = [True , True , True , True ]
	
	print(gate_and(off), gate_and(mid), gate_and(on))
	print(gate_or (off), gate_or (mid), gate_or (on))
	print(gate_xor(off), gate_xor(mid), gate_xor(on))

