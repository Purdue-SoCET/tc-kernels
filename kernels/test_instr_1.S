// add
// 6 + 9 = 15 -> x1
addi.i x1, x0, 6
addi.i x2, x0, 9
add.i x1, x1, x2
// 9 + -12 = -3 -> x2
addi.i x3, x0, -12
add.i x2, x2, x3
// -12 + -25 = -37 -> x3
addi.i x4, x0, -25
add.i x3, x3, x4

// sub
// 9 - 13 = -4 -> x4
addi.i x4, x0, 9
addi.i x5, x0, 13
sub.i x4, x5, x4
// 13 - -20 = 33 -> x5
addi.i x6, x0, -20
sub.i x5, x5, x6

// xor
addi.i x7, x0, -1
// -1 ^ 0 = -1 -> x7
xor.i x7, x0, x7

// or
addi.i x8, x0, 12
addi.i x9, x0, 5
// 12 | 5 = 13 -> x8
or.i x8, x8, x9

// and
addi.i x10, x0, 11
// 5 & 11 = 1 -> x9
and.i x9, x9, x10

// sll
// -1 << 1 = -2 -> x10
sll.i x10, x7, x9

// srl
// -1 >> 1 = 2147483647 -> x11
srl.i x11, x7, x9

// sra
// -2 >> 1 = -1 -> x12
sra.i x12, x10, x9
// 4 >> 1 = 2 -> x13
sra.i x13, x4, x9

// slt
// -20 < 0 -> 1 -> x14
slt.i x14, x6, x0

// sltu
// 33 < -20 = 1 -> x15
sltu.i x15, x5, x6

// mul
// ~~~~~~ 
// NOTE: Does not run due to no opcode, as multiplication is 
// not in base integer RISC-V spec and is in the RV64M multiply extension
// ~~~~~~
// 33 * -37 = -1221 -> x16
// mul.i x16, x5, x3

// mov
// ~~~~~~
// NOTE: Causes assembly error
// ~~~~~~
// mov.i x17, x11

// xori
// 15 ^ -1 = -16 -> x18
xori.i x18, x1, -1

// ori
// 15 | 1024 = 1039 -> x19
ori.i x19, x1, 0x400

// andi
// -16 & 15 = 0 -> x20
andi.i x20, x18, 15

// slli
// 1039 << 4 = 16624 -> x21
slli.i x21, x19, 4

// srli
// -16 >> 1 = 2147483640 -> x22
srli.i x22, x18, 1

// srai
// -37 >> 2 = -9 -> x23
// ~~~~~~~
// Note : Incorrectly assembled as srli
// ~~~~~~~
srai.i x23, x3, 2

// slti
// -37 > 4 = 1 -> x24
// ~~~~~~~
// Note : Incorrectly assembled as addi
// ~~~~~~~
slti.i x24, x3, 4

// sltui
// 16624 < -5 = 1 -> x25
sltui.i x25, x21, -5

// Branch
// If beq, bne, blt, and bge are all working, then x26 - x29 will be 1
beq.i x0, x1, escape
addi.i x26, x0, 1
bne.i x9, x14, escape
addi.i x27, x0, 1
blt.i x1, x6, escape
addi.i x28, x0, 1
bge.i x0, x9, escape
addi.i x29, x0, 1
escape:

beq.i x6, x6, beq_b
addi.i x26, x26, 1
halt
beq_b:
bne.i x0, x1, bne_b
addi.i x27, x27, 1
halt
bne_b:
blt.i x6, x0, blt_b
addi.i x28, x28, 1
halt
blt_b:
bge.i x21, x1, bge_b
addi.i x29, x29, 1
halt
bge_b:


// lui
// lui -1 -> 2^12 - 1 = -4096 -> x30
// ~~~~~~~
// NOTE: must use hex format for negative numbers
// ~~~~~~~
lui.i x30, 0xFFFFF

halt
