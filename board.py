#!/usr/bin/python


import pygame as gm


from components import Port


class Board:
	
	def __init__ (self, background, wires=[], components=[]):
		self.screen = gm.Surface(background.get_size())
		self.back   = background
		self.wires  = wires
		self.comps  = []
		self.ports  = []
		
		#print("{} objects instanciated".format(len(wires) + len(components)))
		
		# split port into a different groups so that
		# they are given a list of input values from the board
		for c in components:
			(self.ports if isinstance(c, Port) else self.comps).append(c)
	
	
	def get_size (self):
		return self.screen.get_size()
	
	
	# update the board with the provided values
	def update (self, values=[]):
		# [!] update wires first
		for wire in self.wires: wire.update()
		for comp in self.comps: comp.update()
		for port in self.ports:
			outs = port.update(values)
	
	
	# optimized drawing function
	def draw (self, window, size, keep_ratio=False):
		
		# draw on the screen first
		self.screen.blit(self.back, (0, 0))
		for wire in self.wires: wire.draw(self.screen)
		for comp in self.comps: comp.draw(self.screen)
		for port in self.ports: port.draw(self.screen)
		
		if keep_ratio:
			window.blit(gm.transform.scale(self.screen, size), (0, 0))
		else:
			window.blit(gm.transform.scale(self.screen, size), (0, 0))
		gm.display.update()

	
	
