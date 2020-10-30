#!/usr/bin/python


def get_value_of_inputs (inputs=[]):
	for i in inputs:
		if i.was_active:
			return True
	return False


def set_value_of_outputs (outputs=[], value=False):
	for o in outputs:
		o.activate(value)
	return value


# base class for building components
class Component:
	
	# generate a new logic gate
	def __init__ (self, position=(0,0), stamp_off=None, stamp_on=None, inputs=[], outputs=[]):
		self.active    = False
		self.position  = position
		self.stamp_off = stamp_off
		self.stamp_on  = stamp_on
		
		# [?] we don't use the list(dict.fromkeys([])) 
		# to keep the same order of elements.
		
		# add outputs first for higher priority
		self.outputs = []
		for o in outputs:
			if not o in self.outputs:
				self.outputs.append(o)
		
		# add inputs second
		self.inputs = []
		for i in inputs:
			if not i in self.outputs and not i in self.inputs:
				self.inputs.append(i)
	
	
	# update the state of the logic gate and connected wires
	def update (self):
		pass
	
	
	# draw the background of the wire once
	def draw_background (self, background):
		background.blit(self.stamp_off, self.position)
		self.stamp_off = None # release
	
	
	# draw the foreground if necessary
	def draw (self, screen):
		if self.active: screen.blit(self.stamp_on, self.position)


