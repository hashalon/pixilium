#!/usr/bin/python


import yaml
import struct
import pygame as gm

from const import *



class Config:
	
	# default configuration
	def __init__ (self):
		
		# default size of the window when created
		self.window_size = (512, 512)
		
		# keep the aspect ratio of the circuit
		# such that pixels stay square
		self.keep_ratio = True
		
		# specify how fast the board refreshes
		self.refresh_rate = 60
		
		# specify how much an extra cell on a clock affect its tickrate
		self.clock_tickrate = 10
		
		# inputs used to interact with the circuits
		self.input_keys = [
			gm.K_1,
			gm.K_2,
			gm.K_3,
			gm.K_4,
			gm.K_5,
			gm.K_6,
			gm.K_7,
			gm.K_8,
			gm.K_9,
			gm.K_0
		]
		
		# colors palettes
		self.palette_low = [
			(0x00, 0x00, 0x00), # BLOCK
			(0x40, 0x40, 0x40), # CROSS
			(0x40, 0x40, 0x00), # WIRE
			(0x40, 0x40, 0x40), # LIGHT
			(0x80, 0x00, 0x00), # AND
			(0x00, 0x80, 0x00), # OR
			(0x30, 0x30, 0x80), # XOR
			(0x00, 0x80, 0x80), # NAND
			(0x80, 0x00, 0x80), # NOR
			(0x80, 0x80, 0x00), # XNOR
			(0x00, 0x40, 0x80), # IO PORT
			(0x40, 0x00, 0x80), # CLOCK
			(0x80, 0x40, 0x00), # T--LATCH
			(0x60, 0xb0, 0x00), # RS-LATCH
			(0x80, 0x00, 0x40), # D--LATCH
			(0x00, 0x80, 0x40), # JK-LATCH
			(0x00, 0x40, 0x00), # MEMORY
			(0x40, 0x00, 0x00)  # JUMPER
		]
		self.palette_high = [
			(0x00, 0x00, 0x00), # BLOCK
			(0x40, 0x40, 0x40), # CROSS
			(0xff, 0xff, 0x80), # WIRE
			(0xff, 0xff, 0xff), # LIGHT
			(0xff, 0x00, 0x00), # AND
			(0x00, 0xff, 0x00), # OR
			(0x30, 0x30, 0xff), # XOR
			(0x00, 0xff, 0xff), # NAND
			(0xff, 0x00, 0xff), # NOR
			(0xe0, 0xe0, 0x00), # XNOR
			(0x00, 0x80, 0xff), # IO PORT
			(0x80, 0x00, 0xff), # CLOCK
			(0xff, 0x80, 0x00), # T--LATCH
			(0x80, 0xff, 0x00), # RS-LATCH
			(0xff, 0x00, 0x80), # D--LATCH
			(0x00, 0xff, 0x80), # JK-LATCH
			(0x00, 0x40, 0x00), # MEMORY
			(0x40, 0x00, 0x00)  # JUMPER
		]
	
	
	# load colors from the PNG palette
	#def load_from_palette (self, plt):
	#	nb = min(len(self.palette), len(plt) / 3)
	#	for i in range(nb):
	#		j = i * 3
	#		color = (plt[j], plt[j + 1], plt[j + 2])
	#		self.palette[i] = color
	
	
	# load config from YAML file
	def load_from_file (self, config_file):
		with open(config_file, 'r') as file:
			config = yaml.load(file)
			
			size = config.get('default window size', None)
			if size: self.window_size = (size.get('x', 512), size.get('y', 512))
			
			self.keep_ratio   = config.get('keep aspect ratio', self.keep_ratio)
			self.refresh_rate = config.get('refresh rate', self.refresh_rate)
			
			palettes = config.get('palettes', {})
			load_color_list(palettes.get('low' , []), self.palette_low )
			load_color_list(palettes.get('high', []), self.palette_high)
	
	
	# return the colors to use for each type of object
	def get_colors (self, pixel):
		return self.palette_low [pixel], self.palette_high[pixel]



# copy a list of colors into the config
def load_color_list (colors_in, colors_out):
	
	# load as many colors as possible
	nb_colors = min(len(colors_in), len(colors_out))
	for i in range(nb_colors):
		
		# analyze input string
		str_in = colors_in[i]
		
		# if string starts with '#', remove it
		if str_in.startswith('#'): str_in = str_in[1:]
			
		# if hex string is of the format #000
		if len(str_in) == 3:
			str_in = ''.join([c * 2 for c in str_in])
			
		# convert hex string into a tuple
		colors_out[i] = struct.unpack('BBB', bytes.fromhex(str_in))



