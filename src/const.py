#!/usr/bin/python


# define the different types of pixel value to analyze
BLOCK = 0
CROSS = 1
WIRE  = 2
LIGHT = 3

GATE_AND  = 4
GATE_OR   = 5
GATE_XOR  = 6
GATE_NAND = 7
GATE_NOR  = 8
GATE_XNOR = 9

IO_PORT = 10
CLOCK   = 11

LATCH_T  = 12
LATCH_RS = 13
LATCH_D  = 14
LATCH_JK = 15

MEMORY = 16
JUMPER = 17


WIRE_TYPES = [
	WIRE ,
	LIGHT
]
GATE_TYPES = [
	GATE_AND ,
	GATE_OR  ,
	GATE_XOR ,
	GATE_NAND,
	GATE_NOR ,
	GATE_XNOR
]
LATCH_TYPES = [
	LATCH_T ,
	LATCH_RS,
	LATCH_D ,
	LATCH_JK
]


def get_value_of_inputs (inputs=[]):
	for i in inputs:
		if i.was_active:
			return True
	return False


def set_value_of_outputs (outputs=[], value=False):
	for o in outputs:
		o.activate(value)
	return value
