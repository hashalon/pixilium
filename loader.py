#!/usr/bin/python


import numpy  as np
import pygame as gm
from scipy.ndimage.measurements import label
from scipy import signal


from const  import *
from wire   import Wire
from gate   import Gate
from port   import Port
from board  import Board
from config import Config


# analyze indexed data to build a logic circuit
def build (data, config=Config()):
	wires, wire_map = make_circuitry(data, config)
	gates = []
	for gtype in GATE_TYPES:
		gates += make_logic_gates(data, gtype, wire_map, wires, config)
	
	ports = make_io_ports(data, wire_map, wires, config)
	
	# TODO: further analyze here...
	
	background = gm.Surface((data.shape[1], data.shape[0]))
	background.fill(config.get_colors(BLOCK))
	background.blit(make_sprite(data == CROSS, config.get_colors(CROSS)), (0, 0))
	
	wires = list(dict.fromkeys(wires)) # purge duplicate occurences
	return Board(background, wires, gates, ports, config.keep_ratio)


# kernel to distinguish inputs from outputs when building logic gates
KERNEL = np.array([
	[0, 1, 0],
	[1, 4, 1], # [!] high value in the middle
	[0, 1, 0]
])

# number of neighboring pixels to consider a wire an input or an output
NEIGHBORS_INPUT  = 1
NEIGHBORS_OUTPUT = 3


# generate the IO ports
def make_io_ports (data, wire_map, wires=[], config=Config()):
	ports = [] # of generated io ports
	nb_wires = len(wires)
	
	# generate labels for ports
	port_data, port_map = make_wire_data(data, IO_PORT, config)
	
	# for each gate find to which wires it is connected
	for i in range(len(port_data)):
		
		io_map = signal.convolve(port_map == i + 1, KERNEL, mode='same')
		coords_out = np.fliplr(np.transpose(
			np.where(io_map == NEIGHBORS_OUTPUT)))
		
		# connect output wires second (lower priority)
		outputs = []
		for x, y in coords_out:
			label = wire_map[y, x] - 1
			if 0 <= label < nb_wires:
				output = wires[label]
				if not output in outputs: outputs.append(output)
				
		pos, spr_off, spr_on = port_data[i]
		ports.append(Port(outputs, pos, spr_off, spr_on))
		
	return ports


# generate the logic gates
def make_logic_gates (data, gtype, wire_map, wires=[], config=Config()):
	gates = [] # list of generated gates
	nb_wires = len(wires)
	
	# generate labels and sprites for all gates
	gate_data, gate_map = make_wire_data(data, gtype, config)
		
	# for each gate find to which wires it is connected
	for i in range(len(gate_data)):
			
		# build a new gate
		pos, spr_off, spr_on = gate_data[i]
		gate = Gate(gtype, pos, spr_off, spr_on)
		gates.append(gate)
		
		io_map = signal.convolve(gate_map == i + 1, KERNEL, mode='same')
		
		coords_in  = np.transpose(np.where(io_map == NEIGHBORS_INPUT ))
		coords_out = np.transpose(np.where(io_map == NEIGHBORS_OUTPUT))
		
		# for each port, connect the wire to the gate
		# connect input wires first so they have priority
		for y, x in coords_in:
			label = wire_map[y, x] - 1
			if 0 <= label < nb_wires:
				gate.add_input(wires[label])
		
		# connect output wires second (lower priority)
		for y, x in coords_out:
			label = wire_map[y, x] - 1
			if 0 <= label < nb_wires:
				gate.add_output(wires[label])
	
	return gates


# build the circuitry to connect components
def make_circuitry (data, config=Config()):
	wires = []
	wmap  = np.zeros(data.shape, dtype=int)
	
	# for each type of wires generate objects for them
	for wtype in WIRE_TYPES:
		wire_data, wire_map = make_wire_data(data, wtype, config)
		wmap += wire_map + (data == wtype) * len(wires)
		
		for t in wire_data:
			wires.append(Wire().add_sprite(t[0], t[1], t[2]))
	
	# connect them with cross sections
	group_wires(data, wmap, wires)
	group_wires(data, wmap, wires, True)
	
	return wires, wmap


# there is a nasty bug here...
# group connected wires togethers
def group_wires (data, wire_map, wires=[], transpose=False):
	if transpose:
		data     = data    .transpose()
		wire_map = wire_map.transpose()
	
	# generate mapping between wires and indexes
	mapping  = {}
	nb_wires = len(wires)
	for i in range(nb_wires):
		wire = wires[i]
		mapping[wire] = mapping.get(wire, []) + [i]
	
	# iterate over each row
	for y in range(data.shape[1]):
		previous = -1
		crossing = False
		
		# for each cell in this row
		for x in range(data.shape[0]):
			cell  = data    [x, y]
			label = wire_map[x, y]
			
			# if cell is a wire
			if cell in WIRE_TYPES:
			
				# if we encountered CROSS cells, 
				# the two wires are different and valid
				if (crossing and previous != label 
					and 0 < label    <= nb_wires 
					and 0 < previous <= nb_wires):
					
					# merge the two wires into one
					# and replace the old wire by the new one at all indexes
					old = wires[previous - 1]
					new = wires[label    - 1].merge(old)
					for i in mapping[old]: wires[i] = new
					mapping[new] += mapping[old]
				
				previous = label
				crossing = False
			
			# if cell is a cross section
			elif cell == CROSS: crossing = True
			else: # if cell is any other cell
				previous = -1
				crossing = False
	
	# return the new reduced list of wires
	return wires



# generate wires used in the program
def make_wire_data (data, wtype, config=Config()):
	wire_data = [] # list of wires generated
	sprites   = {} # store pairs of colored sprites identified by hash
	
	# map of wires with labels
	wire_map, nb_wires = label(data == wtype)
	
	# for each individual wire
	for i in range(nb_wires):
		
		# extract wire as minimal matrix
		mask = wire_map == (i + 1)
		bbox = make_bounding_box(mask)
		wire = mask[bbox[0]:bbox[1], bbox[2]:bbox[3]]
		hsh  = make_hash(wire)
		
		# generate only one sprite for each wire pattern
		if not hsh in sprites:
			colors = config.get_colors(wtype)
			sprites[hsh] = make_sprites(wire, colors)
		
		# add the wire data to the list
		spr_off, spr_on = sprites[hsh]
		wire_data.append(( (bbox[2], bbox[0]), spr_off, spr_on ))
	
	# return the list of wire data, and the wire map
	return wire_data, wire_map


# find the bounding box around a blob in a numpy matrix
def make_bounding_box (blob):
	rows = np.any(blob, axis=1)
	cols = np.any(blob, axis=0)
	rmin, rmax = np.where(rows)[0][[0, -1]]
	cmin, cmax = np.where(cols)[0][[0, -1]]
	return rmin, rmax+1, cmin, cmax+1


# generate a unique hash for each wire pattern
def make_hash (wire, wtype=0):
	width  = bytes([wtype, wire.shape[0]]) # width of the pattern 
	serial = np.packbits(wire.flatten()).tostring() # serialized pattern
	return width + serial


# generate colored sprites for the wire
def make_sprites (bool_map, colors=[]):
	sprites = []
	
	# generate a base pattern for the sprite
	im = bool_map.transpose()
	pattern = gm.surfarray.make_surface(im * 0xff)
	pattern.set_colorkey((0, 0, 0))
	
	# generate a new sprite for each color
	for color in colors:
		sprite = gm.Surface(im.shape, gm.SRCALPHA)
		sprite.blit(pattern, (0, 0))
		sprite.fill(color, special_flags=gm.BLEND_RGBA_MULT)
		sprites.append(sprite)
	
	return sprites


def make_sprite (bool_map, color=(0xff, 0xff, 0xff)):
	im = bool_map.transpose()
	pattern = gm.surfarray.make_surface(im * 0xff)
	sprite  = gm.Surface(im.shape, gm.SRCALPHA)
	sprite.blit(pattern, (0, 0))
	sprite.fill(color, special_flags=gm.BLEND_RGBA_MULT)
	return sprite



