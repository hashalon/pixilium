#!/usr/bin/python


import itertools

from components.component import Component


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

