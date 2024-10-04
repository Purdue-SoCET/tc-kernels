mnist: 
//Assume fully connected network, 784 input size, hidden layer 16, output 10

// W1(16 ,768) x X(768, 1) -> A1(16, 1)
// Weight address, input address, result address, (n = 16, k = 768, m = 1) needed for tiled matrix mult.
// Assume weight address, input address, result address are on the stack
POP x3      // W1 address
POP x4      // Input address
POP x5      // A1 address
// In reverse order as read in tiledmatmult: 
ldi x6, 1
PUSH x6     // m
ldi x6, 768
PUSH x6     // k
ldi x6, 16
PUSH x6     // n
PUSH x5     // A1 address
PUSH x4     // Input address
PUSH x3     // W1 address
beq x0, x0, tiledmatmul

// A1(16, 1) + B1(16, 1) -> C1
mov x7, x5 // Pointer to A1 temp value
POP x8     // Pointer to B1 temp value
ldi x9, 0  // Index count
Loop_b1: 
ld x10, x7
ld x11, x9
fp_add x11, x10, x10 // Floating point addition??
st x11, ?? //C1 address
addi x8, x8, 1
beq x8, x6, Loop_b1

// ReLU(C1) -> X2(16, 1)

// W2(10, 16) x X2(16, 1) -> A2(10, 1)

// A2+(10, 1) + B2(10, 1) -> C2

// ReLU(C2) -> Result