#!/usr/bin/python


import itertools


from const import *


# base class for building components
class Component:
	
	# generate a new logic gate
	def __init__ (self, position=(0,0), stamp_off=None, stamp_on=None, inputs=[], outputs=[]):
		self.active    = False
		self.position  = position
		self.stamp_off = stamp_off
		self.stamp_on  = stamp_on
		
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


# logic gates
class Gate (Component):
	
	# generate a new logic gate
	def __init__ (self, cell_type, position=(0,0), stamp_off=None, stamp_on=None, inputs=[], outputs=[]):
		super().__init__(position, stamp_off, stamp_on, inputs, outputs)
		self.operation = GATE_FUNCTIONS[cell_type]

	
	# update the state of the logic gate and connected wires
	def update (self):
		values = [inpt.was_active for inpt in self.inputs]
		self.active = self.operation(values)
		for outpt in self.outputs:
			outpt.activate(self.active)
	

# input/output ports
class Port (Component):
	
	# update the values on each individual output wire
	def update (self, values=[]):
		
		# process values leaving the port
		self.active = True in values
		for output, value in itertools.zip_longest(self.outputs, values, fillvalue=False):
			if output: output.activate(value)
		
		# process values entering the port
		return [inpt.was_active for inpt in self.inputs]


# emit signal every X tick
class Clock (Component):
	
	# generate a new logic gate
	def __init__ (self, ticks, position=(0,0), stamp_off=None, stamp_on=None, inputs=[], outputs=[]):
		super().__init__(position, stamp_off, stamp_on, inputs, outputs)
		self.counter = 0
		self.ticks   = ticks

	
	# update the state of the logic gate and connected wires
	def update (self):
		
		# detect if one of the inputs is active
		self.active = False
		for inpt in self.inputs:
			if inpt.was_active:
				self.active = True
				break
		
		# check if the Clock should emit a signal or not
		activate = False
		if not self.active:
			self.counter += 1
			if self.counter >= self.ticks:
				activate     = True
				self.active  = True
				self.counter = 0
		
		# transmit signal to outputs
		for outpt in self.outputs:
			outpt.activate(activate)


# the four kinds of latch
class ToggleLatch (Component):
	
	# update the values on each individual output wire
	def update (self):
		values = [inpt.was_active for inpt in self.inputs]
		
		# toggle the value of active
		if True in values: self.active = not self.active
		
		for outpt in self.outputs:
			outpt.activate(self.active)
		


