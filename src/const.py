#!/usr/bin/python

# 
# [ 0] empty
# [ 1] wire red
# [ 2] wire green
# [ 3] wire yellow
# [ 4] wire blue
# [ 5] wire magenta
# [ 6] wire cyan
# [ 7] wire RGB

# [ 8] cross section
# [ 9] gate AND  (red    )
# [10] gate OR   (green  )
# [11] gate XNOR (yellow )
# [12] gate XOR  (blue   )
# [13] gate NOR  (magenta)
# [14] gate NAND (cyan   )
# [15] port IO

# [16] memory
# [17] T -latch (red    )
# [18] D -latch (green  )
# [19] JK-latch (yellow )
# [20] RS-latch (blue   )
# [21] clock    (magenta)
# [22] delay    (cyan   )
# [23] 

# [24] compressor (bool* -> int)
# [25] gate ADD (&SUB)  (red    )
# [26] gate MUL (&DIV)  (green  )
# [27] gate MUL (&MOD)  (yellow )
# [28] gate POW         (blue   )
# [29] gate ROT <<left  (magenta)
# [30] gate ROT >>right (cyan   )
# [31] deplexor (int -> bool*)

# [32] block black
# [33] block red
# [34] block green
# [35] block yellow
# [36] block blue
# [37] block magenta
# [38] block cyan
# [39] block white


# define the different types of pixel value to analyze
EMPTY   = 0x00
LIGHT   = 0x07
CROSS   = 0x08
PORT_IO = 0x0F
MEMORY  = 0x10

CONV_BOOL2INT = 0x18
CONV_INT2BOOL = 0x1F

GATE_AND  = 0x09
GATE_OR   = 0x0A
GATE_XOR  = 0x0C
GATE_NAND = 0x0E
GATE_NOR  = 0x0D
GATE_XNOR = 0x0B

LATCH_T  = 0x11
LATCH_D  = 0x12
LATCH_RS = 0x14
LATCH_JK = 0x13

OP_ADD_SUB = 0x19
OP_MUL_DIV = 0x1A
OP_MUL_MOD = 0x1B
OP_POW     = 0x1C
OP_ROT_L   = 0x1D
OP_ROT_R   = 0x1E

WIRE_TYPES = [0x1, 0x2, 0x3, 0x4, 0x5, 0x6, LIGHT]
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
	LATCH_D ,
	LATCH_RS,
	LATCH_JK
]
OP_TYPES = [
	OP_ADD_SUB,
	OP_MUL_DIV,
	OP_MUL_MOD,
	OP_POW    ,
	OP_ROT_L  ,
	OP_ROT_R
]
BLOCK_TYPES = [0x20, 0x21, 0x22, 0x23, 0x24, 0x25, 0x26, 0x27]


def get_value_of_inputs (inputs=[]):
	for i in inputs:
		if i.was_active:
			return True
	return False


def set_value_of_outputs (outputs=[], value=False):
	for o in outputs:
		o.activate(value)
	return value
