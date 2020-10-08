#!/usr/bin/python


import pygame as gm
import itertools


from wire import Wire
from gate import Gate


class Board:
	
	def __init__ (self, background, wires=[], gates=[], inputs=[], keep_ratio=True):
		self.screen     = gm.Surface(background.get_size())
		self.background = background
		self.wires      = wires
		self.gates      = gates
		self.inputs     = inputs
		self.keep_ratio = keep_ratio
		
	
	# update the board with the provided values
	def update (self, values=[]):
		for inpt, value in itertools.zip_longest(self.inputs, values, fillvalue=False):
			if inpt: inpt.active = value
			
		for wire in self.wires: wire.update()
		for gate in self.gates: gate.update()
	
	# draw the board to the screen
	def draw (self, window, size):
		# draw on the screen first
		self.screen.blit(self.background, (0, 0))
		for gate in self.gates: gate.draw(self.screen)
		for wire in self.wires: wire.draw(self.screen)
		
		if self.keep_ratio:
			window.blit(gm.transform.scale(self.screen, size), (0, 0))
		else:
			window.blit(gm.transform.scale(self.screen, size), (0, 0))
		gm.display.update()
