# ISA
## Data types
| type | suffix | format | description
| ---- | ------ | ------ | -----------
| matrix | `.m` | 4x4 array of FP16 | The matrix data type for the systolic array
| int | `.i` | 32 bit signed integer | 

## Integer Instructions
| Instr | Name | Description | 
| ----- | ---- | ----------- | 
| `add.i` | ADD | `rd = rs1 + rs2` | 
| `sub.i` | SUB | `rd = rs1 - rs2` | 
| `xor.i` | XOR | `rd = rs1 ^ rs2` |
| `or.i` | OR | `rd = rs1 OR rs2` |
| `and.i` | AND | `rd = rs1 & rs2` | 
| `sll.i` | Shift Left Logical | `rd = rs1 << rs2` |
| `srl.i` |Shift Right Logical | `rd = rs1 >> rs2` |
| `sra.i` |Shift Right Arith | `rd = rs1 >> rs2` |
| `slt.i` |Set Less Than | `rd = (rs1 < rs2)?1:0` |
| `sltu.i` | Set Less Than (U) | `rd = (rs1 < rs2)?1:0` |
| `mul.i` | Multiply | `rd = (rs1 * rs2)[31:0]` | 
| `mov.i` | Move | `rd = rs1` | 
| `addi.i` | ADD Immediate | `rd = rs1 + imm` | 
| `xori.i` | XOR Immediate | `rd = rs1 ^ imm` |
| `ori.i` | OR Immediate | `rd = rs1 OR imm` |
| `andi.i` | AND Immediate | `rd = rs1 & imm` | 
| `slli.i` | Shift Left Logical Imm| `rd = rs1 << imm[0:4]` |
| `srli.i` |Shift Right Logical Imm| `rd = rs1 >> imm[0:4]` |
| `srai.i` |Shift Right Arith Imm| `rd = rs1 >> imm[0:4]` |
| `slti.i` |Set Less Than | `rd = (rs1 < imm)?1:0` |
| `sltui.i` | Set Less Than Imm (U) | `rd = (rs1 < imm)?1:0` |
| `beq.i` |Branch == B | ` if(rs1 == rs2) PC += imm` |
| `bne.i` |Branch != B | ` if(rs1 != rs2) PC += imm` |
| `blt.i` |Branch < B  | `if(rs1 < rs2) PC += imm` |
| `bge.i` |Branch ≥ B  | `if(rs1 >= rs2) PC += imm` |
| `ld.i` | Load | `rd = M[rs1 + imm]` | 
| `lui.i` | Load Upper Imm| `rd = imm << 12` | 
| `st.i` | Store | `M[rs1 + imm] = rd` | 
| `jal` | Jump And Link | `rd = PC+4; PC += imm` |
| `jalr`| Jump And Link Reg | `rd = PC+4; PC = rs1 + imm`|

## Matrix Instructions
| Instr | Name | Description | 
| ----- | ---- | ----------- | 
| `ld.m` | Load Matrix | `md = M[rs1]` | 
| `st.m` | Store Matrix | `M[rs1] = md` | 
| `gemm.m` | Matrix Multiply | `md = ma @ mb + mc` | 

## Psuedo-instructions
| Instr | Description | Pseudo Instruction |
| ----- | ----------- | ----------|
| `PUSH` | `sub + sw`|`sp = sp - 4; M[sp] <= R[rs1]`| 
| `POP` | `add + lw`|`sp = sp + 4; R[rs2] <= M[sp]`| 
| `NOP` | no operation|`addi.i x0, x0, 0`| 
| `HALT` | halt|`halt`|
