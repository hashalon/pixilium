# Pixilium
A little toy program for building logic circuits from PNG images.

Pixilium is a toy program intended to simulate the behavior of a die of silicium. The program takes as an input an indexed PNG image and analyze it to run a graphical simulation of the circuitry that is drawn on it.

## Specifications
The program analyze the image by reading the index value of each pixel, with each index corresponding to a specific component.


Index | Name | Function
------|------|---------
 0 | Empty     | an empty cell, does nothing
 1 | Cross     | Allow to cross wires without connecting them
 2 | Wire      | Wire to connect components together
 3 | Light     | Wire that is brighter (intended for displays)
 4 |  AND Gate | Perform an AND operation on the inputs
 5 |   OR Gate | Perform an OR  operation on the inputs
 6 |  XOR Gate | Perform an XOR operation on the inputs
 7 | NAND Gate | Perform an NAND operation on the inputs
 8 |  NOR Gate | Perform an NOR  operation on the inputs
 9 | XNOR Gate | Perform an XNOR operation on the inputs
10 | IO Port   | Allow to transmit keyboard's inputs into the circuit
11 | Clock     | Emit a signal every X ticks
12 |  T-Latch  | Togglable memory cell
13 | RS-Latch  | Flip-Flop memory cell
14 |  D-Latch  | Memory cell that retain a value if it is unlocked
15 | JK-Latch  | Universal memory cell
16 | Memory    | Store multiple bits into a 2D matrix


Wires of different types (Wire and Light) and components of different types cannot connect directly.

To connect a wire as an input to a component, they need to touch by atleast one pixel either horizontally or vertically (diagonals do not count).

To connect a wire as an output of a component, the pixel should be surrounded by exactly three pixels of the component.

In the case of the memory latches D and JK, the unlock signal is received from a input wire that is connected to the component in three or more points.

Cross sections allow to carry the signal of wires horizontally and vertically without connecting them. It can be used to link different types of wires together (connecting a Wire to a Light). Or it can be used to build ROM.

IO Port is used to interact with the circuit. Each output of this component is assigned to a different keyboard key. By default those keys are the number keys from 1 to 0. And they are assigned in reading order (left to right, then up to down).

## Installation
To run this program, you need Python3.x with the librairies *numpy*, *pygame* and *pillow*.
