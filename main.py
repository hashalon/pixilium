#!/usr/bin/python


import sys
from os  import path
from PIL import Image
import numpy  as np
import pygame as gm

import loader
from board  import Board
from config import Config

# fix _imaging module for Pillow
_imaging = Image.core


# main loop
def main (data, config=Config()):
	
	# generate a board that can be updated
	board = loader.build_circuit_board(data, config)
	
	# build a resizable window
	size   = config.window_size
	window = gm.display.set_mode(size, gm.RESIZABLE)
	clock  = gm.time.Clock()
	tick   = config.refresh_rate
	keys   = config.input_keys
	
	values   = [False for k in keys]
	running  = True
	resizing = False
	while running:
		for evt in gm.event.get():
			if   evt.type == gm.QUIT: running = False
			elif evt.type == gm.KEYDOWN:
				if evt.key in keys:
					values[keys.index(evt.key)] = True
			elif evt.type == gm.KEYUP:
				if evt.key in keys:
					values[keys.index(evt.key)] = False
			
			elif evt.type == gm.VIDEORESIZE:
				size = evt.dict['size']
				resizing = True
			elif evt.type == gm.ACTIVEEVENT:
				if resizing:
					window = gm.display.set_mode(size, gm.RESIZABLE)
					resizing = False
		
		clock.tick(tick)
		if not resizing:
			board.update(values)
			board.draw(window, size)


# entry point of the program
if __name__ == "__main__":
	if len(sys.argv) >= 2: 
		input_file = sys.argv[1]
		if path.exists(input_file):
			image = Image.open(input_file)
			data  = np.array(image)
			if data.ndim == 2:
				# successfully opened the PNG file
				
				# try to load a config too
				config = Config()
				
				# load a default palette from the picture itself
				config.load_from_palette(image.getpalette())
				
				# analyze command line arguments
				if len(sys.argv) >= 3:
					config_file = sys.argv[2]
					if path.exists(config_file):
						config.load_from_file(config_file)
				
				# run the program
				main(data, config)
				
			else: print("Loaded picture is not an indexed PNG.")
		else: print("Input file does not exists.")
	else: print("No input file provided.")
