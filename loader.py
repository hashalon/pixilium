#!/usr/bin/python


import numpy  as np
import pygame as gm
from scipy.ndimage.measurements import label
from scipy import signal
# use following kernel:
# [[0, 1, 0]
#  [1, 4, 1]
#  [0, 1, 0]]
# wire is output if neighbor count == 3, input if count == 1 or 2
# (+4 at the center so that pixels belonging to the component itself are directly ignored)

#from skimage.morphology import disk, dilation
# https://stackoverflow.com/questions/47371787/counting-neighbors-in-matrix-conway-game-of-life

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
	
	background = gm.Surface(data.shape)
	background.fill(config.get_colors(BLOCK))
	background.blit(make_sprite(data == CROSS, config.get_colors(CROSS)), (0, 0))
	
	
	return Board(background, 
		list(dict.fromkeys(wires)), gates, ports, config.keep_ratio)


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
	# generate labels and sprites for all wires and lights
	wire_data1, wire_map1 = make_wire_data(data, WIRE , config)
	wire_data2, wire_map2 = make_wire_data(data, LIGHT, config)
	
	# merge the two maps into one
	wire_map = wire_map1 + wire_map2 + (wire_map2 != 0) * len(wire_data1)
	
	# instanciate the wires to connect them together
	wires = []
	for d in wire_data1 + wire_data2:
		wires.append(Wire().add_sprite(d[0], d[1], d[2]))
	
	# connect them with cross sections
	crosses = data == CROSS
	group_wires(crosses, wire_map, wires)
	group_wires(crosses, wire_map, wires, True)
	
	return wires, wire_map


# group connected wires togethers
def group_wires (crosses, wire_map, wires=[], transpose=False):
	if transpose:
		crosses  = crosses .transpose()
		wire_map = wire_map.transpose()
	
	# iterate over each row
	height = min(crosses.shape[0], wire_map.shape[0])
	width  = min(crosses.shape[1], wire_map.shape[1])
	for i in range(height):
	
		# find intervals for each CROSS sequence
		linecrss = np.concatenate(([0], crosses[i], [0]))
		absdiff  = np.abs(np.diff(linecrss))
		ranges   = np.where(absdiff == True)[0].reshape(-1, 2)
		
		# find the labels to connect together
		line_wire  = wire_map[i]
		for range_ in ranges:
			imin, imax = range_
			if 0 < imin and imax < width - 1:
				a = line_wire[imin - 1] - 1
				b = line_wire[imax] - 1
				wires[b] = wires[a].merge(wires[b])
	
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
			sprites[hsh] = make_sprites(wire, colors[0], colors[1])
		
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
	

# generate two colored sprites for the wire
def make_sprites (bool_map, 
	color_off = (0x00, 0x00, 0x00), 
	color_on  = (0xff, 0xff, 0xff)):
	
	im = bool_map.transpose()
	pattern = gm.surfarray.make_surface(im * 0xff)
	pattern.set_colorkey((0x00, 0x00, 0x00))
	
	spr_off = gm.Surface(im.shape, gm.SRCALPHA)
	spr_on  = gm.Surface(im.shape, gm.SRCALPHA)
	spr_off.blit(pattern, (0, 0))
	spr_on .blit(pattern, (0, 0))
	
	spr_off.fill(color_off, special_flags=gm.BLEND_RGBA_MULT)
	spr_on .fill(color_on , special_flags=gm.BLEND_RGBA_MULT)
	
	return spr_off, spr_on


def make_sprite (bool_map, color=(0xff, 0xff, 0xff)):
	im = bool_map.transpose()
	pattern = gm.surfarray.make_surface(im * 0xff)
	sprite  = gm.Surface(im.shape, gm.SRCALPHA)
	sprite.blit(pattern, (0, 0))
	sprite.fill(color, special_flags=gm.BLEND_RGBA_MULT)
	return sprite

