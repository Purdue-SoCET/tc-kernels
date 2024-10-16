// Basic Matmul Tensor Core Kernel

lw.i %r1, 0[%sp] // input matrix start address
lw.i %r2, 4[%sp] // weight matrix start address
lw.i %r3, 4[%sp] // output matrix start address
ori.i %r4, 4 // stride
ld.m %m1, 0[%r1], %r3 // load the input matrix
ld.m %m2, 0[%r2], %r3 // load the weight matrix
mm.m %m3, %m1, %m2, %m0 // run the matrix multiplication
sw.m %m3, 0[%r3], %r4 // store the output matrix
halt