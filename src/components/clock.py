#!/usr/bin/python

from const import get_value_of_inputs, set_value_of_outputs

from components.component import Component


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


