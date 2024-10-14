mnist: 
// MLP, 784 input size, hidden layer size 16, output size 10

// W1(16 ,768) x I(768, 1) + B1(16, 1) -> A1(16, 1)
// W1 address, I address, A1 address, (n = 16, k = 768, m = 1) needed for tiled matrix mult.
// Assume addresses are passed as function parameters in x10-x12 according to tiledmatmul in this order
// B1 is stored in result memory for accumulator preloading
addi.i x13, x0, 16
addi.i x14, x0, 768
addi.i x15, x0, 1

PUSH x12               // Modified by tiledmatmul, so needs to be saved to stack

jal x1, tiledmatmul

// ReLU(A1) -> X1(16, 1)
mv.i x9, x12           // Move result address

relu_loop:
li.i x4, 0             // Counter i in [0, n - 1]
li.i x6, 0x0080        // Right FP16 sign mask
slli.i x5, 8           // Left FP16 sign mask
lw.i x7, 0(x9)         // Load 2 FP16 values [left, right]
mv.i x8, x7            // Copy both
srli.i x7, x7, 8    
slli.i x7, x7, 8       // Left value only in left spot
slli.i x8, x8, 8    
srli.i x8, x8, 8       // Right value only in right spot
and.i x5, x5, x7       // x5 now stores 0 if left > 0
and.i x6, x6, x8       // x6 now stores 0 if right > 0
beq x5, x0, positive_left 
andi.i x7, x7, 0x00FF  // Left value becomes 0
positive_left:
beq x6, x0, positive_right
li.i x6, 0x00FF
slli.i x6, x6, 8
and.i x8, x8, x6       // Right value becomes 0
positive_right:
or.i x7, x7, x8        // Concatenate left and right values
sw.i x7, 0(x9)         // Write ReLU(left | right) to memory
addi.i x9, 4
addi.i x4, x4, 1
bne x4, x13, relu_loop

// W2(10, 16) x X1(16, 1) -> A2(10, 1)
// Assume W2 address is stored in x16
// Assume A2 address is stored in x17, preloaded with B2
POP x12
mv.i x10, x16          // W2 address is now in weight address
mv.i x11, x12          // X1 address is now in input address
mv.i x12, x17          // A2 address is now in result address
addi.i x13, x0, 10     // n = 10
addi.i x14, x0, 16     // k = 16, m is still 1

jal x1, tiledmatmul

ret
