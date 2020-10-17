#!/usr/bin/python


import itertools


from const import *


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
		set_value_of_outputs(self.outputs, self.active)
	

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
		self.active = get_value_of_inputs(self.inputs)
		
		# check if the Clock should emit a signal or not
		activate = False
		if not self.active:
			self.counter += 1
			if self.counter >= self.ticks:
				activate     = True
				self.active  = True
				self.counter = 0
		
		# transmit signal to outputs
		set_value_of_outputs(self.outputs, activate)


# how many contact points there should be to concider a input as a clock
NB_CONTACTS_CLOCK_INPUT = 3


# the four kinds of latch
class Latch (Component):
	
	# complete override to count 
	def __init__ (self, cell_type, position=(0,0), stamp_off=None, stamp_on=None, inputs=[], outputs=[]):
		self.active    = False
		self.position  = position
		self.stamp_off = stamp_off
		self.stamp_on  = stamp_on
		self.prev_in1  = False
		self.prev_in2  = False
		
		# add outputs first for higher priority
		outs = []
		for o in outputs:
			if not o in outs:
				outs.append(o)
		self.outputs1 = outs[ ::2]
		self.outputs2 = outs[1::2]
		
		# count the number of contacts for each input
		counts = {}
		for i in inputs:
			if not i in outs:
				counts[i] = counts.get(i, 0) + 1
		
		# sort inputs based on the number of contact points
		ins = []
		self.clocks = []
		for i in inputs:
			count = counts.get(i, 0)
			if count >= NB_CONTACTS_CLOCK_INPUT:
				self.clocks.append(i)
				del counts[i]
			elif 0 < count:
				ins.append(i)
				del counts[i]
		self.inputs1 = ins[ ::2]
		self.inputs2 = ins[1::2]
		
		# get the operation to use based on the type of the cell
		self.operation = LATCH_FUNCTIONS[cell_type]
	
	# update the values on each individual output wire
	def update (self):
		clock  = get_value_of_inputs(self.clocks )
		value1 = get_value_of_inputs(self.inputs1)
		value2 = get_value_of_inputs(self.inputs2)
		
		self.active = self.operation(value1, value2, clock, self.active, self.prev_in1, self.prev_in2)
		self.prev_in1 = value1
		self.prev_in2 = value2
		
		set_value_of_outputs(self.outputs1,     self.active)
		set_value_of_outputs(self.outputs2, not self.active)


