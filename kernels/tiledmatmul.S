tiledmatmul:        // Y = W x I + B
// x10              // weight W address
// x11              // input  I address
mv.i x18, x11      
// x12              // result Y address, where B is preloaded
mv.i x19, x12
// x13              // n
// x14              // k
// x15              // m

li.i x21, 2        //   Number of bytes in an element
mul.i x21, x21, 4   // x sys. arr. height
mul.i x21, x21, 3   // x sys. arr. width - 1
mul.i x21, x21, x14 // x k = memory offset for next weight matrix tile [tile_row (matrix_row 1), 0] -> [tile_row + 1, 0]

li.i x22, 2        //   Number of bytes in an element
mul.i x22, x22, 4   // x sys. arr. height
mul.i x22, x22, 3   // x sys. arr. width - 1
mul.i x22, x22, x15 // x m = memory offset for next input matrix tile [tile_row (matrix_row 1), 0] -> [tile_row + 1, 0]

li.i x23, 2        //   Number of bytes in an element
mul.i x23, x23, 4   // x sys. arr. height
mul.i x23, x23, 4   // x sys. arr. width
mul.i x23, x23, x15 // x m = memory offset for next result matrix row

li.i x4, 0         // Temp result tile row = temp weight tile row = 0 

Loop_row:  
li.i x5, 0         // Result tile sum term = weight tile column = 0 
mv.i x11, x18       // Reset x11 to [0, 0] of input matrix 

Loop_term_idx:  
li.i x6, 0         // Result tile column = 0 
mv.i x12, x19       // Reset x12 to [row, 0] of result matrix
ld.m m1, x10        // Load new weight tile 

Loop_column: 
ld.m m2, x11        // Load new input tile 
ld.m m3, x12        // Load partial sum for column 
gemm.m m3, m1, m2, m3 
st.m m3, x12        // Save new partial sum back to result memory
addi.i x11, x11, 8  // Move x11 to next column of input matrix
addi.i x12, x12, 8  // Find address of next partial sum from result memory
addi.i x6, x6, 1 
bne x6, x15, Loop_column 

addi.i x10, x10, 8  // Move x10 next column of weight matrix 
add.i x11, x11, x22 // Move x11 to [row + 1, 0] of input matrix 
addi.i x5, x5, 1 
bne x5, x14, Loop_term_idx 

                    // Result row is done
add.i x19, x19, x23 // Find address of next completed row 
add.i x10, x10, x21 // Move x10 to [row + 1, 0] of weight matrix 
addi.i x4, x4, 1 
bne x4, x13, Loop_row 

ret
