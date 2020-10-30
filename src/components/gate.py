#!/usr/bin/python


from const import *
from components.component import Component


# boolean operations
def gate_nand (values): return not gate_and(values)
def gate_nor  (values): return not gate_or (values)
def gate_xnor (values): return not gate_xor(values)
def gate_and  (values): return not (False in values)
def gate_or   (values): return True in values
def gate_xor  (values): return values.count(True) == len(values) / 2


GATE_FUNCTIONS = {
	GATE_AND  : gate_and ,
	GATE_OR   : gate_or  ,
	GATE_XOR  : gate_xor ,
	GATE_NAND : gate_nand,
	GATE_NOR  : gate_nor ,
	GATE_XNOR : gate_xnor
}


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
	
