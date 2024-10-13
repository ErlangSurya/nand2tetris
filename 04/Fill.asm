// This file is part of www.nand2tetris.org
// and the book "The Elements of Computing Systems"
// by Nisan and Schocken, MIT Press.
// File name: projects/4/Fill.asm

// Runs an infinite loop that listens to the keyboard input. 
// When a key is pressed (any key), the program blackens the screen,
// i.e. writes "black" in every pixel. When no key is pressed, 
// the screen should be cleared.

(ALL)
@SCREEN
D=A
@R1 //loop counter for coloring. Begin at 16384
M=D //initialize R1=16384
(LOOP)
@KBD
D=M //check if keyboard is pressed
@COLORING
D;JNE
@R1
D=M
A=D //Pick the correct pixel
M=0 // Set color to white
@PIXELOVER
0;JMP
(COLORING) 
@R1
D=M
A=D //Pick the correct pixel
M=-1 // Set color to black
(PIXELOVER)
@R1
M=M+1 // loop counter increment
D=M
@24575
D=D-A 
@LOOP
D;JLT // Check if R1-24575<0
@ALL
0;JMP