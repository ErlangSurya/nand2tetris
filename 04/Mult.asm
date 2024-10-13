// This file is part of www.nand2tetris.org
// and the book "The Elements of Computing Systems"
// by Nisan and Schocken, MIT Press.
// File name: projects/4/Mult.asm

// Multiplies R0 and R1 and stores the result in R2.
// (R0, R1, R2 refer to RAM[0], RAM[1], and RAM[2], respectively.)
// The algorithm is based on repetitive addition.

//// Replace this comment with your code.


@R2
M=0  //output=0
(LOOP)
@R1
D=M  //D=R1
@END
D;JLE //Done if R1=0
@R1
M=M-1 // R1=R1-1
@R0
D=M
@R2
M=D+M // output += R0
@LOOP
0;JMP
(END)
@END
0;JMP