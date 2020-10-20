# Pixilium
A little toy program for building logic circuits from PNG images.

Pixilium is a toy program intended to simulate the behavior of a die of silicium. The program takes as an input an indexed PNG image and analyze it to run a graphical simulation of the circuitry that is drawn on it.

## Specifications
The program analyze the image by reading the index value of each pixel, with each index corresponding to a specific component. (The order of components may change in future versions)


Index | Name | Function
------|------|---------
 0 | Empty     | an empty cell, does nothing
 1 | AND Gate  | Perform an AND operation on the inputs
 2 | OR  Gate  | Perform an OR  operation on the inputs
 3 | XOR Gate  | Perform an XOR operation on the inputs
 4 | IO Port   | Allow to transmit keyboard's inputs into the circuit
 5 | T  Latch  | Togglable memory cell
 6 | RS Latch  | Flip-Flop memory cell
 7 | Wire      | Wire to connect components together
 8 | Cross     | Allow to cross wires without connecting them
 9 | NAND Gate | Perform an NAND operation on the inputs
10 | NOR  Gate | Perform an NOR  operation on the inputs
11 | XNOR Gate | Perform an XNOR operation on the inputs
12 | Clock     | Emit a signal every X ticks
13 | D  Latch  | Memory cell that retain a value if it is unlocked
14 | JK Latch  | Universal memory cell
15 | Light     | Wire that is brighter (intended for displays)


Wires of different types (Wire and Light) and components of different types cannot connect directly.

To connect a wire as an input to a component, they need to touch by atleast one pixel either horizontally or vertically (diagonals do not count).

To connect a wire as an output of a component, the pixel should be surrounded by exactly three pixels of the component.

In the case of the memory latches D and JK, the unlock signal is received from a input wire that is connected to the component in three or more points.

Cross sections allow to carry the signal of wires horizontally and vertically without connecting them. It can be used to link different types of wires together (connecting a Wire to a Light). Or it can be used to build ROM.

IO Port is used to interact with the circuit. Each output of this component is assigned to a different keyboard key. By default those keys are the number keys from 1 to 0. And they are assigned in reading order (left to right, then up to down).

## Installation
To run this program, you need Python3.x with the librairies *numpy*, *pygame* and *pillow*.
