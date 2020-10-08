#!/usr/bin/python


import pygame as gm


FPS = 60


def draw (window, sprite, clock):
	window.blit(gm.transform.scale(sprite, (128, 128)), (0, 0))
	gm.display.update()
	


def main ():
	run = True
	sprite = gm.image.load('test.png')
	clock  = gm.time.Clock()
	window = gm.display.set_mode((128, 128), gm.RESIZABLE)
	
	while run:
		clock.tick(FPS)
		draw(window, sprite, clock)
		
		for event in gm.event.get():
			if event.type == gm.QUIT:
				run = False


# test rendering empty frame
if __name__ == "__main__":
	main()
