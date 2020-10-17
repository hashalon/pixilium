#!/usr/bin/python


import numpy  as np
import pygame as gm
from scipy.ndimage.measurements import label
from scipy import signal


from const      import *
from wire       import Wire
from components import *
from board      import Board
from config     import Config


# analyze indexed data to build a logic circuit
def build_circuit_board (data, config=Config()):
	
	# weave the wires into the circuit board
	wires, label_map = weave_wires(data, config)
	
	# solder the components to the board
	components = solder_components(data, label_map, wires, config)
	
	# purge duplicate occurences
	wires = list(dict.fromkeys(wires))
	
	# make a new background for the board
	background = draw_background(data, wires + components, config)
	
	return Board(background, wires, components)


# draw the background used by the board
def draw_background (data, objects=[], config=Config()):
	# generate the main canvas
	height, width = data.shape
	background = gm.Surface((width, height))
	background.fill(config.get_colors(BLOCK)[0])
	
	# draw cross sections
	crosses = make_stamps(data == CROSS, config.get_colors(CROSS))[0]
	background.blit(crosses, (0, 0))
	
	# draw the off state of all dynamic objects
	for obj in objects: obj.draw_background(background)
	
	return background


# this is the minimal size a component can have
MIN_COMP_SIZE = 5


def solder_components (data, label_map, wires=[], config=Config()):
	# generate the components
	components = []
	
	# build the logic gates
	for gtype in GATE_TYPES:
		tuples = prepare_components(data, gtype, label_map, wires, config)
		for pos, stamp, nb, ins, outs in tuples:
			if nb >= MIN_COMP_SIZE:
				components.append( Gate(gtype, pos, stamp[0], stamp[1], ins, outs) )
	
	# build IO ports
	tuples = prepare_components(data, IO_PORT, label_map, wires, config)
	for pos, stamp, nb, ins, outs in tuples:
		if nb >= MIN_COMP_SIZE:
			components.append( Port(pos, stamp[0], stamp[1], ins, outs) )
	
	# build clocks
	tuples = prepare_components(data, CLOCK, label_map, wires, config)
	for pos, stamp, nb, ins, outs in tuples:
		if nb >= MIN_COMP_SIZE:
			ticks = (nb - MIN_COMP_SIZE) * config.clock_tickrate
			if ticks <= 0: ticks = 2
			components.append( Clock(ticks, pos, stamp[0], stamp[1], ins, outs) )
	
	# build the memory latches
	for ltype in LATCH_TYPES:
		tuples = prepare_components(data, ltype, label_map, wires, config)
		for pos, stamp, nb, ins, outs in tuples:
			if nb >= MIN_COMP_SIZE:
				components.append( Latch(ltype, pos, stamp[0], stamp[1], ins, outs) )
	
	return components
	


# kernel to distinguish inputs from outputs when building logic gates
KERNEL = np.array([
	[0, 1, 0],
	[1, 4, 1], # [!] high value in the middle
	[0, 1, 0]
])

# number of neighboring pixels to consider a wire an input or an output
NEIGHBORS_INPUT  = 1
NEIGHBORS_OUTPUT = 3


# generate the logic gates
def prepare_components (data, cell_type, wire_label_map, wires=[], config=Config()):
	components = [] # list of generated gates
	nb_labels  = len(wires)
	
	# generate labels and stamps for all components
	tuples, label_map = parse_data(data, cell_type, config)
	
	# generate a matrix of the location of wires
	wire_map = wire_label_map > 0
		
	# for each gate find to which wires it is connected
	for i in range(len(tuples)):
		
		# find inputs and outputs based on number of neighbors
		pattern = label_map == i + 1
		
		# count the number of cells used by the component
		nb_cells = np.count_nonzero(pattern)
		
		# order IOs in a left->right, up->down fashion
		io_map = signal.convolve(pattern, KERNEL, mode='same') * wire_map
		coords_in  = np.transpose(np.where(io_map == NEIGHBORS_INPUT ))
		coords_out = np.transpose(np.where(io_map == NEIGHBORS_OUTPUT))
		
		# for each port, connect the wire to the component
		# connect input wires first so they have priority
		inputs = []
		for y, x in coords_in:
			label = wire_label_map[y, x] - 1
			if 0 <= label < nb_labels:
				inputs.append(wires[label])
		
		# connect output wires second (lower priority)
		outputs = []
		for y, x in coords_out:
			label = wire_label_map[y, x] - 1
			if 0 <= label < nb_labels:
				outputs.append(wires[label])
		
		# add the new tuple to the list
		components.append( tuples[i] + (nb_cells, inputs, outputs) )
		
	return components


# build the circuitry to connect components
def weave_wires (data, config=Config()):
	wires = []
	label_map  = np.zeros(data.shape, dtype=int)
	
	# for each type of wires generate objects for them
	for wtype in WIRE_TYPES:
		tuples, sub_map = parse_data(data, wtype, config)
		label_map += sub_map + (data == wtype) * len(wires)
		
		for position, stamp in tuples:
			wires.append(Wire().add_stamp(position, stamp[0], stamp[1]))
	
	# connect them with cross sections
	link_wires(data, label_map, wires, False)
	link_wires(data, label_map, wires, True )
	
	return wires, label_map


# group connected wires togethers
def link_wires (data, label_map, wires=[], transpose=False):
	if transpose:
		data      = data     .transpose()
		label_map = label_map.transpose()
	
	# generate mapping between wires and indexes
	mapping  = {}
	nb_labels = len(wires)
	for i in range(nb_labels):
		wire = wires[i]
		mapping[wire] = mapping.get(wire, []) + [i]
	
	# iterate over each row
	for y in range(data.shape[1]):
		prev_label = -1
		crossing   = False
		
		# for each cell in this row
		for x in range(data.shape[0]):
			cell_type = data     [x, y]
			label     = label_map[x, y]
			
			# if cell is a wire
			if cell_type in WIRE_TYPES:
			
				# if we encountered CROSS cells, 
				# the two wires are different and valid
				if (crossing and prev_label != label 
					and 0 < label      <= nb_labels 
					and 0 < prev_label <= nb_labels):
					
					# merge the two wires into one
					# and replace the old wire by the new one at all indexes
					old = wires[prev_label - 1]
					new = wires[label      - 1].merge(old)
					for i in mapping[old]: wires[i] = new
					mapping[new] += mapping[old]
				
				prev_label = label
				crossing   = False
			
			# if cell is a cross section
			elif cell_type == CROSS: crossing = True
			else: # if cell is any other cell
				prev_label = -1
				crossing   = False
	
	# return the new reduced list of wires
	return wires



# return a list of tuples and the associated label map
def parse_data (data, cell_type, config=Config()):
	tuples = [] # list of tuples in label's order
	stamps = {} # store pairs of colored stamps identified by hash
	
	# map of wires with labels
	label_map, nb_objects = label(data == cell_type)
	
	# for each individual wire
	for i in range(nb_objects):
		
		# extract wire as minimal matrix
		mask = label_map == (i + 1)
		y1, y2, x1, x2 = make_bounding_box(mask)
		pattern = mask[y1:y2, x1:x2]
		hash_p  = make_hash(pattern)
		
		# optimize the total number of stamps generated
		if not hash_p in stamps:
			colors = config.get_colors(cell_type)
			stamps[hash_p] = make_stamps(pattern, colors)
		
		# add the wire data to the list
		stamp = stamps[hash_p]
		tuples.append(( (x1, y1), stamp ))
	
	# return the list of instanciated objects
	return tuples, label_map


# find the bounding box around a blob in a numpy matrix
def make_bounding_box (pattern):
	rows = np.any(pattern, axis=1)
	cols = np.any(pattern, axis=0)
	rmin, rmax = np.where(rows)[0][[0, -1]]
	cmin, cmax = np.where(cols)[0][[0, -1]]
	return rmin, rmax+1, cmin, cmax+1


# generate a unique hash for each pattern
def make_hash (pattern, cell_type=0):
	head   = bytes([cell_type, pattern.shape[0]])      # type and width 
	serial = np.packbits(pattern.flatten()).tostring() # serialized pattern
	return head + serial


# generate colored stamps for objects
def make_stamps (pattern, colors=[]):
	stamps = []
	
	# generate a base stamp
	tmp = gm.surfarray.make_surface(pattern.transpose() * 0xff)
	tmp.set_colorkey((0, 0, 0))
	
	# generate a new stamp for each color
	for color in colors:
		stamp = gm.Surface(tmp.get_size(), gm.SRCALPHA)
		stamp.blit(tmp, (0, 0))
		stamp.fill(color, special_flags=gm.BLEND_RGBA_MULT)
		stamps.append(stamp)
	
	return stamps

