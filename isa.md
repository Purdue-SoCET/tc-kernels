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
| `addi.i` | ADD Immediate | `rd = rs1 + imm` | 
| `xori.i` | XOR Immediate | `rd = rs1 ^ imm` |
| `ori.i` | OR Immediate | `rd = rs1 OR imm` |
| `andi.i` | AND Immediate | `rd = rs1 & imm` | 
| `slli.i` | Shift Left Logical Imm| `rd = rs1 << imm[0:4]` |
| `srli.i` |Shift Right Logical Imm| `rd = rs1 >> imm[0:4]` |
| `srai.i` |Shift Right Arith Imm| `rd = rs1 >> imm[0:4]` |
| `slti.i` |Set Less Than | `rd = (rs1 < imm)?1:0` |
| `sltui.i` | Set Less Than Imm (U) | `rd = (rs1 < imm)?1:0` |
| `ld.i` | Load x| `x` | 
| `st.i` | Store x | `x` | 

## Matrix Instructions
| Instr | Name | Description | 
| ----- | ---- | ----------- | 
| `ld.m` | Load Matrix | `md = M[rs1]` | 
| `st.m` | Store Matrix | `M[rs1] = md` | 
| `gemm.m` | Matrix Multiply | `md = ma @ mb + mc` | 

## Psuedo-instructions
| Instr | Description | 
| ----- | ----------- | 
| `PUSH` | `x` | 
| `POP` | `x` | 
| `NOP` | `x` | 
