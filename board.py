#!/usr/bin/python


import pygame as gm

from wire import Wire
from gate import Gate


class Board:
	
	def __init__ (self, background, wires=[], gates=[], ports=[], keep_ratio=True):
		self.screen     = gm.Surface(background.get_size())
		self.background = background
		self.wires      = wires
		self.gates      = gates
		self.ports      = ports
		self.keep_ratio = keep_ratio
		
		print("{} Wires".format(len(wires)))
		print("{} Gates".format(len(gates)))
		print("{} Ports".format(len(ports)))
		
		# draw all elements background
		self.draw_background()
		
	
	# update the board with the provided values
	def update (self, values=[]):
		for wire in self.wires: wire.update()
		for gate in self.gates: gate.update()
		for port in self.ports: port.update(values)
	
	# draw the board to the screen
	def draw (self, window, size):
		
		# draw on the screen first
		self.screen.blit(self.background, (0, 0))
		for port in self.ports: port.draw(self.screen)
		for gate in self.gates: gate.draw(self.screen)
		for wire in self.wires: wire.draw(self.screen)
		
		if self.keep_ratio:
			window.blit(gm.transform.scale(self.screen, size), (0, 0))
		else:
			window.blit(gm.transform.scale(self.screen, size), (0, 0))
		gm.display.update()
	
	
	# optimized drawing function
	def draw_foreground (self, window, size):
		
		# draw on the screen first
		self.screen.blit(self.background, (0, 0))
		for port in self.ports: port.draw_foreground(self.screen)
		for gate in self.gates: gate.draw_foreground(self.screen)
		for wire in self.wires: wire.draw_foreground(self.screen)
		
		if self.keep_ratio:
			window.blit(gm.transform.scale(self.screen, size), (0, 0))
		else:
			window.blit(gm.transform.scale(self.screen, size), (0, 0))
		gm.display.update()
	
	
	# draw the board to the screen
	def draw_background (self):
		for port in self.ports: port.draw_background(self.background)
		for gate in self.gates: gate.draw_background(self.background)
		for wire in self.wires: wire.draw_background(self.background)
	
	
