#!/usr/bin/python


import numpy  as np
import pygame as gm
from scipy.ndimage.measurements import label

from const  import *
from wire   import Wire
from gate   import Gate
from board  import Board
from config import Config


# analyze indexed data to build a logic circuit
def build (data, config=Config()):
	wires, wire_map = make_circuitry(data, config)
	gates = make_logic_gates(data, wires, wire_map, config)
	inputs = []
	
	# TODO: use PASS gates as inputs at first
	for g in gates:
		if g.gtype == GATE_PASS:
			inputs += g.inputs
	
	# TODO: further analyze here...
	
	background = gm.Surface(data.shape)
	background.fill(config.get_colors(BLOCK))
	
	return Board(background, 
		list(dict.fromkeys(wires)), gates, inputs, config.keep_ratio)



# generate the logic gates
def make_logic_gates (data, wires, wire_map, config=Config()):
	sprites = {}
	gates   = []
	
	height, width = data.shape
	padded = np.pad(wire_map, [(1, 1), (1, 1)])
	
	# iterate over each pixel and try to find logic gates
	for x in range(width - 2):
		for y in range(height - 2):
			# extract two 5x5 sub matrices		
			gate = analyze_sub_gate_matrices (
				data  [y:y + 3, x:x + 3],
				padded[y:y + 5, x:x + 5],
				sprites, wires, (x, y), config)
			
			# if a gate was generated, add it to the list
			if gate != None: gates.append(gate)
	
	# return the list of gates generated
	return gates


# analyze the sub matrices provided and deduce the behaviour of the logic gate in it
def analyze_sub_gate_matrices (sub_gate, sub_wire, 
	sprites={}, wires=[], position=(0, 0), config=Config()):
	
	# test if we have the four corners of a logic gate
	gtype = sub_gate[0, 0]
	if (gtype in GATE_TYPES 
		and gtype == sub_gate[2, 0]
		and gtype == sub_gate[0, 2]
		and gtype == sub_gate[2, 2]
		and gtype == sub_gate[1, 1]):
				
		# generate a new logic gate object
		gate = Gate(gtype, position) # TODO add sprites...

		# test which sides are input and which are output
		# | 1 2 |  .  | 1 3 |  .  | 3 4 |  .  | 2 4 |
		# | 3 4 |  .  | 2 4 |  .  | 1 2 |  .  | 1 3 |
		sides = [
			(sub_gate[0, 1], sub_wire), 
			(sub_gate[1, 0], sub_wire.transpose()), 
			(sub_gate[2, 1], np.flipud(sub_wire)), 
			(sub_gate[1, 2], np.fliplr(sub_wire).transpose())
		]
		for side_g, side_w in sides:
			if side_g != gtype: # output
				connect_gate_to_wire(gate, wires, side_w[1, 2], False)
			else: # input
				connect_gate_to_wire(gate, wires, side_w[0, 1])
				connect_gate_to_wire(gate, wires, side_w[0, 2])
				connect_gate_to_wire(gate, wires, side_w[0, 3])
		
		# if the gate is connected to inputs and outputs it is valid
		if gate.is_connected():
			pattern = sub_gate == gtype
			
			# generate only one pair sprite for every pattern encountered
			hsh = make_hash(pattern, gtype)
			if not hsh in sprites:
				colors = config.get_colors(gtype)
				sprites[hsh] = make_sprites(pattern, colors[0], colors[1])
				
			gate.sprite_off, gate.sprite_on = sprites[hsh]
			return gate
	
	# no gate here
	return None


# check if the label matches a wire and connect the gate to it
def connect_gate_to_wire (gate, wires, label, is_input=True):
	if 0 < label <= len(wires):
		if is_input: gate.add_input (wires[label - 1])
		else       : gate.add_output(wires[label - 1])



# build the circuitry to connect components
def make_circuitry (data, config):
	# generate labels and sprites for all wires and lights
	sprites   = {}
	wires     = []
	wire_map  = make_wires(data, WIRE , sprites, wires, config)
	wire_map += make_wires(data, LIGHT, sprites, wires, config)
	
	# connect them with cross sections
	crosses = data == CROSS
	group_wires(crosses, wire_map, wires)
	group_wires(crosses, wire_map, wires, True)
	
	return wires, wire_map


# group connected wires togethers
def group_wires (crosses, wire_map, wires, transpose=False):
	if transpose:
		crosses  = crosses .transpose()
		wire_map = wire_map.transpose()
	
	# iterate over each row
	height = min(crosses.shape[0], wire_map.shape[0])
	width  = min(crosses.shape[1], wire_map.shape[1])
	for i in range(height):
	
		# find intervals for each CROSS sequence
		line_cross = np.concatenate(([0], crosses[i], [0]))
		absdiff = np.abs(np.diff(line_cross))
		ranges  = np.where(absdiff == True)[0].reshape(-1, 2)
		
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
def make_wires (data, wtype, sprites={}, wires=[], config=Config()):
	shift = len(wires)
	
	# map of wires with labels
	wire_map, nb_wires = label(data == wtype)
	
	# for each individual wire
	for i in range(nb_wires):
		
		# extract wire as minimal matrix
		wire = wire_map == i + 1
		bbox = make_bounding_box(wire)
		wire = wire[bbox[0]:bbox[1], bbox[2]:bbox[3]]
		hsh  = make_hash(wire, wtype)
		
		# generate only one sprite for each wire pattern
		if not hsh in sprites:
			colors = config.get_colors(wtype)
			sprites[hsh] = make_sprites(wire, colors[0], colors[1])
		
		# add the newly generate wire to the list
		spr_off, spr_on = sprites[hsh]
		wire = Wire().add_sprite((bbox[2], bbox[0]), spr_off, spr_on)
		wires.append(wire)
	
	if shift == 0: return wire_map
	else: return wire_map + (wire_map != 0) * shift
	

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
def make_sprites (wire, 
	color_off = (0x00, 0x00, 0x00), 
	color_on  = (0xff, 0xff, 0xff)):
	
	im = wire.transpose()
	pattern = gm.surfarray.make_surface(im * 0xff)
	pattern.set_colorkey((0x00, 0x00, 0x00))
	
	spr_off = gm.Surface(im.shape, gm.SRCALPHA)
	spr_on  = gm.Surface(im.shape, gm.SRCALPHA)
	spr_off.blit(pattern, (0, 0))
	spr_on .blit(pattern, (0, 0))
	
	spr_off.fill(color_off, special_flags=gm.BLEND_RGBA_MULT)
	spr_on .fill(color_on , special_flags=gm.BLEND_RGBA_MULT)
	
	return spr_off, spr_on


if __name__ == "__main__":
	window = gm.display.set_mode((128, 128))
	window.fill((255, 0, 0))
	
	data = np.array([
		[4, 7, 4, 0],
		[7, 4, 4, 7],
		[4, 4, 4, 0],
		[0, 7, 0, 0]
	])
	
	board = build(data)
	board.draw(window, (128, 128))
	
	#spr1, spr2 = make_sprites(data == 4, (0,0,128), (0,0,255))
	#window.blit(gm.transform.scale(spr1, (32, 32)), (0, 0))
	#window.blit(gm.transform.scale(spr2, (32, 32)), (64, 64))
	gm.display.update()
	
	clock  = gm.time.Clock()
	running = True
	while running:
		for evt in gm.event.get():
			if evt.type == gm.QUIT: running = False
		clock.tick(10)
	
	


