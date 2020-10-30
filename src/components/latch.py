#!/usr/bin/python


from const import *
from components.component import Component


# how many contact points there should be to concider a input as a clock
NB_CONTACTS_CLOCK_INPUT = 3


# latches behaviors
def latch_t (in1, in2, clock, prev, prev_in1, prev_in2):
	return not prev if (in1 or in2) and not (prev_in1 or prev_in2) else prev

def latch_rs (in1, in2, clock, prev, prev_in1, prev_in2):
	in1 = in1 and not prev_in1
	in2 = in2 and not prev_in2
	
	if in1 and in2: return not prev # toggle every frame
	elif in1: return True
	elif in2: return False
	else: return prev

def latch_d (in1, in2, clock, prev, prev_in1, prev_in2):
	return in1 or in2 if clock else prev

def latch_jk (in1, in2, clock, prev, prev_in1, prev_in2):
	return latch_rs(in1, in2, clock, prev, prev_in1, prev_in2) if clock else prev


LATCH_FUNCTIONS = {
	LATCH_T  : latch_t ,
	LATCH_RS : latch_rs,
	LATCH_D  : latch_d ,
	LATCH_JK : latch_jk
}


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

