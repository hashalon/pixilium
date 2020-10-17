#!/usr/bin/python


# define the different types of pixel value to analyze
BLOCK     = 0x0
GATE_AND  = 0x1
GATE_OR   = 0x2
GATE_XOR  = 0x3
IO_PORT   = 0x4
LATCH_T   = 0x5
LATCH_D   = 0x6
WIRE      = 0x7
CROSS     = 0x8
GATE_NAND = 0x9
GATE_NOR  = 0xA
GATE_XNOR = 0xB
CLOCK     = 0xC
LATCH_RS  = 0xD
LATCH_JK  = 0xE
LIGHT     = 0xF

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


# boolean operations
def gate_nand (values): return not gate_and(values)
def gate_nor  (values): return not gate_or (values)
def gate_xnor (values): return not gate_xor(values)
def gate_and  (values): return not (False in values)
def gate_or   (values): return True in values
def gate_xor  (values): return values.count(True) == len(values) / 2


GATE_FUNCTIONS = {
	GATE_AND  : gate_and ,
	GATE_OR   : gate_or  ,
	GATE_XOR  : gate_xor ,
	GATE_NAND : gate_nand,
	GATE_NOR  : gate_nor ,
	GATE_XNOR : gate_xnor
}


# latches behaviors

def latch_t (in1, in2, clock, prev, prev_in1, prev_in2):
	return not prev if (in1 or in2) and not (prev_in1 or prev_in2) else prev

def latch_rs (in1, in2, clock, prev, prev_in1, prev_in2):
	in1 = in1 and not prev_in1
	in2 = in2 and not prev_in2
	
	if in1 and in2: return not prev # toggle every frame
	elif in1: return True
	elif in2: return False
	else: return prev

def latch_d (in1, in2, clock, prev, prev_in1, prev_in2):
	return in1 or in2 if clock else prev

def latch_jk (in1, in2, clock, prev, prev_in1, prev_in2):
	return latch_rs(in1, in2, clock, prev, prev_in1, prev_in2) if clock else prev


LATCH_FUNCTIONS = {
	LATCH_T  : latch_t ,
	LATCH_RS : latch_rs,
	LATCH_D  : latch_d ,
	LATCH_JK : latch_jk
}
