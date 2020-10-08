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
		
		# specify if we use a simpler color palette
		self.use_four_colors = False
		
		# colors palettes
		self.mini_palette = [
			(0x00, 0x00, 0x00), # low
			(0x40, 0x40, 0x40), # high
			(0x80, 0x80, 0x80), # low
			(0xff, 0xff, 0xff), # high
		]
		self.palette = [
			(0x00, 0x00, 0x00), # BLACK   | BLOCK    | CROSS
			(0x80, 0x00, 0x00), # RED     | AND      | NAND
			(0x00, 0x80, 0x00), # GREEN   | OR       | NOR
			(0x80, 0x80, 0x00), # YELLOW  | XOR      | XNOR
			(0x00, 0x00, 0x80), # BLUE    | IO       | CLOCK
			(0x80, 0x00, 0x80), # MAGENTA | T  LATCH | D  LATCH
			(0x00, 0x80, 0x80), # CYAN    | RS LATCH | JK LATCH
			(0x80, 0x80, 0x80), # WHITE   | WIRE     | LIGHT
			
			(0x40, 0x40, 0x40), # BLACK   | BLOCK    | CROSS
			(0xff, 0x00, 0x00), # RED     | AND      | NAND
			(0x00, 0xff, 0x00), # GREEN   | OR       | NOR
			(0xff, 0xff, 0x00), # YELLOW  | XOR      | XNOR
			(0x00, 0x00, 0xff), # BLUE    | IO       | CLOCK
			(0xff, 0x00, 0xff), # MAGENTA | T  LATCH | D  LATCH
			(0x00, 0xff, 0xff), # CYAN    | RS LATCH | JK LATCH
			(0xff, 0xff, 0xff), # WHITE   | WIRE     | LIGHT
		]
	
	
	# load colors from the PNG palette
	def load_from_palette (self, plt):
		nb = min(len(self.palette), len(plt) / 3)
		for i in range(nb):
			j = i * 3
			color = (plt[j], plt[j + 1], plt[j + 2])
			self.palette[i] = color
	
	
	# load config from YAML file
	def load_from_file (self, config_file):
		with open(config_file, 'r') as file:
			config = yaml.load(file)
			
			size = config.get('default window size', None)
			if size: self.window_size = (size.get('x', 512), size.get('y', 512))
			
			self.keep_ratio   = config.get('keep aspect ratio', self.keep_ratio)
			self.refresh_rate = config.get('refresh rate', self.refresh_rate)
			
			colors = config.get('colors', {})
			self.use_four_colors = colors.get('use four colors', False)
			load_color_list(colors.get('mini palette', []), self.mini_palette)
			load_color_list(colors.get('palette'     , []), self.palette     )
	
	
	# return the colors to use for each type of object
	def get_colors (self, pixel):
		if self.use_four_colors:
			plt = self.mini_palette
			if   pixel == BLOCK: return  plt[0]
			elif pixel == WIRE : return [plt[2], plt[3]]
			elif pixel == LIGHT: return [plt[2], plt[3]]
			elif pixel == CROSS: return  plt[1]
			else: return [plt[1], plt[2]]
		else:
			plt = self.palette
			if   pixel == BLOCK: return  plt[BLOCK]
			elif pixel == WIRE : return [plt[CROSS], plt[WIRE ]]
			elif pixel == LIGHT: return [plt[CROSS], plt[LIGHT]]
			elif pixel == CROSS: return  plt[CROSS]
			if pixel >= 8: pixel -= 8
			return [plt[pixel], plt[pixel + 8]]



# copy a list of colors into the config
def load_color_list (colors_in, colors_out):
	
	# load as many colors as possible
	nb_colors = min(len(colors_in), len(colors_out))
	for i in range(nb_colors):
		
		# analyze input string
		str_in = colors_in[i]
		
		# if string is of format #000000
		if str_in.startswith('#'): 
			str_in = str_in[1:]
			
			# if hex string is of the format #000
			if len(str_in) == 3:
				str_in = ''.join([c * 2 for c in str_in])
			
			# convert hex string into a tuple
			colors_out[i] = struct.unpack('BBB', 
				bytes.fromhex(str_in))



