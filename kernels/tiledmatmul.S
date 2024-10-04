tiledmatmul: 
POP x1 // weight address
POP x2 // input address
POP x3 // result address
POP x7 // n 
POP x8 // k 
POP x9 // m

ld.i x10, x1       // Current weight tile address 
ld.i x11, x2       // Current input tile address 
ldi.i x4, 0        // Result tile row = weight tile row = 0 

Loop_row: 
ld.i x11, x2       // Reset x11 to 0,0 of input matrix 
ldi.i x5, 0        // Result tile sum term index = weight tile column = 0 

Loop_term_idx: 
ld.m m0, x10       // Load new weight tile 
ldi.i x6, 0        // Result tile column = 0 

Loop_column: 
ld.m m1, x11       // Load new input tile 
addi.i, x3, x3, ?? // Find address of next partial sum from result memory
ld.m m2, x3        // Load partial sum for column 
gemm m3, m0, m1, m2 
st.m m3, x3        // Save new partial sum back to result memory
aadd.i x11, x11, ??// Move x11 to next col of input matrix –maybe 8nx8k so256 
addi.i x6, x6, 1 
bne x6, x9, Loop_column 

addi.i x5, x5, 1 
add.i x10, x10, ?? // Move x10 next column of weight matrix 
add.i x11, x11, ?? // Move x11 to next row of input matrix 
bne x5, x8, Loop_term_idx 

                   // Result row is done
addi.i x3, ??      // Find address to save next completed row 
add.i x10, x10, ?? // Move x10 to next row of weight matrix 
addi.i x4, x4, 1 
bne x4, x7, Loop_row 

halt
