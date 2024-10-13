tiledmatmul:        // Y = W x I + B
POP x10             // weight W address
POP x20             // input  I address
POP x12             // result Y address, where B is preloaded
POP x7              // n
POP x8              // k
POP x9              // m

ldi.i x21, 2        //   Number of bytes in an element
mul.i x21, x21, 4   // x sys. arr. height
mul.i x21, x21, 3   // x sys. arr. width - 1
mul.i x21, x21, x8  // x k 
addi.i x21, x21, 2  // + 2 = memory offset for weight matrix tile [row, k] -> [row + 1, 0]

ldi.i x22, 2        //   Number of bytes in an element
mul.i x22, x22, 4   // x sys. arr. height
mul.i x22, x22, 4   // x sys. arr. width
mul.i x22, x22, x9  // x m = memory offset to go down row in input matrix

ldi.i x4, 0         // Temp result tile row = temp weight tile row = 0 

Loop_row:  
ld.i x11, x20       // Reset x11 to [0, 0] of input matrix 
ldi.i x5, 0         // Temp result tile sum index = temp weight tile column = 0 

Loop_term_idx:  
ld.m m1, x10        // Load new weight tile 
ldi.i x6, 0         // Result tile column = 0 

Loop_column: 
ld.m m2, x11        // Load new input tile 
addi.i, x12, x12, 2 // Find address of next partial sum from result memory
ld.m m2, x12        // Load partial sum for column 
gemm.m m3, m1, m2, m3 
st.m m3, x12        // Save new partial sum back to result memory
add.i x11, x11, 2   // Move x11 to next column of input matrix
addi.i x6, x6, 1 
bne x6, x9, Loop_column 

add.i x10, x10, 2   // Move x10 next column of weight matrix 
add.i x11, x11, x22 // Move x11 to next row of input matrix 
addi.i x5, x5, 1 
bne x5, x8, Loop_term_idx 

                    // Result row is done
addi.i x12, 2       // Find address to save next completed row 
add.i x10, x10, x21 // Move x10 to [row + 1, 0] of weight matrix 
addi.i x4, x4, 1 
bne x4, x7, Loop_row 

halt
