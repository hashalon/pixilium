#!/usr/bin/python


from const import get_value_of_inputs


# a cursor that can shift in a direction or an other
class Cursor:
	
	# generate a new logic lane
	def __init__ (self, positions=[], color=(0xff, 0xff, 0xff), decrs=[], incrs=[], outputs=[]):
		
		self.cursor = 0
		self.color  = color
		self.decrs  = decrs
		self.incrs  = incrs
		
		self.nb_cells  = min(len(positions), len(outputs))
		self.outputs   = outputs  [0:self.nb_cells]
		self.positions = positions[0:self.nb_cells]
	
	
	# update the state of the logic lane and connected wires
	def update (self):
		
		# find new position of the cursor
		value = self.cursor + self.nb_cells
		if get_value_of_inputs(self.decrs): value -= 1
		if get_value_of_inputs(self.incrs): value += 1
		self.cursor = value % self.nb_cells
		
		# activate the correct output
		self.outputs[self.cursor].activate(True)
	
		
	# draw the foreground if necessary
	def draw (self, screen):
		screen.set_at(self.positions[self.cursor], self.color)
