#!/usr/bin/python


# a matrix of memory cells
class Memory:
	
	# generate a new logic lane
	def __init__ (self, color=(0xff, 0xff, 0xff), 
		pos_trails=[], inputs =[], outputs=[], 
		pos_lanes =[], readers=[], writers=[], 
		horizontal_trails=True):
		
		nb_trails = min(len(pos_trails), len(inputs ), len(outputs))
		nb_lanes  = min(len(pos_lanes ), len(readers), len(writers))
		
		self.color   = color
		self.inputs  = inputs [0:nb_trails]
		self.outputs = outputs[0:nb_trails]
		self.readers = readers[0:nb_lanes ]
		self.writers = writers[0:nb_lanes ]
		
		# generate memory cells with their position
		self.actives   = []
		self.positions = []
		
		pos_trails = pos_trails[0:nb_trails]
		pos_lanes  = pos_lanes [0:nb_lanes]
		cells = [False for _ in range(nb_trails)]
		for g in pos_lanes:
			coords = []
			for l in pos_trails:
				coords.append((g, l) if horizontal_trails else (l, g))
			self.actives  .append(cells )
			self.positions.append(coords)
		
		self.nb_lanes = nb_lanes
	
	
	# update the state of the logic lane and connected wires
	def update (self):
		# read input values
		values = [inpt.was_active for inpt in self.inputs]
		
		# for each trail,
		# if a reader is active, read from input
		# if a writer is active, send to  output
		for i in range(self.nb_lanes):
			cells = self.actives[i]
			if self.readers[i].was_active: self.actives[i] = values
			if self.writers[i].was_active:
				for out, cell in zip(self.outputs, cells):
					out.activate(cell)
	
	
	# draw the foreground if necessary
	def draw (self, screen):
		for a, pos in zip(self.actives, self.positions):
			if a: screen.set_at(pos, self.color)
