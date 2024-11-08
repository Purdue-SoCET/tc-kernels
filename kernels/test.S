addi.i x1, x0, 3
addi.i x2, x0, 0
loop:
    addi.i x2, x2, 1
    halt
    bne.i x1, x2, loop
