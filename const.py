#!/usr/bin/python


# define the different types of pixel value to analyze
BLOCK     = 0x0
GATE_AND  = 0x1
GATE_OR   = 0x2
GATE_XOR  = 0x3
GATE_PASS = 0x4
LATCH_T   = 0x5
LATCH_D   = 0x6
WIRE      = 0x7
CROSS     = 0x8
GATE_NAND = 0x9
GATE_NOR  = 0xA
GATE_XNOR = 0xB
GATE_NOT  = 0xC
LATCH_RS  = 0xD
LATCH_JK  = 0xE
LIGHT     = 0xF


GATE_TYPES = [
	GATE_AND ,
	GATE_OR  ,
	GATE_XOR ,
	GATE_PASS,
	GATE_NAND,
	GATE_NOR ,
	GATE_XNOR,
	GATE_NOT
]
