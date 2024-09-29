ori.i x10, x10, 0
ori.i x4, x4, 1
ori.i x5, x5, 4
lui.i x28, 0xFFFFF
ori.i x14, x14, 0xF00
sub.i x14, x14, x28
ld.i  x16, 0(x14)

loop:
    ld.i  x11, 0(x10)
    ld.i  x12, 4(x10)
    add.i x13, x11, x12
    sw.i  x13, 8(x10)
    add.i x10, x10, x5
    sub.i x16, x16, x4
    bne.i x16, x0, loop

end:
    halt