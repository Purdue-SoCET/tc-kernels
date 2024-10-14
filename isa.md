# ISA
## Data types
| type | suffix | format | description
| ---- | ------ | ------ | -----------
| matrix | `.m` | 4x4 array of FP16 | The matrix data type for the systolic array
| int | `.i` | 32 bit signed integer | 

## Integer Instructions
| Instr | Type | Name | Description | 
| ----- | ---- | ---- | ----------- | 
| `add.i` | R | ADD | `rd = rs1 + rs2` | 
| `sub.i` | R | SUB | `rd = rs1 - rs2` | 
| `xor.i` | R | XOR | `rd = rs1 ^ rs2` |
| `or.i` | R | OR | `rd = rs1 OR rs2` |
| `and.i` | R | AND | `rd = rs1 & rs2` | 
| `sll.i` | R | Shift Left Logical | `rd = rs1 << rs2` |
| `srl.i` | R | Shift Right Logical | `rd = rs1 >> rs2` |
| `sra.i` | R | Shift Right Arith | `rd = rs1 >> rs2` |
| `slt.i` | R | Set Less Than | `rd = (rs1 < rs2)?1:0` |
| `sltu.i` | R | Set Less Than (U) | `rd = (rs1 < rs2)?1:0` |
| `mul.i` | R | Multiply | `rd = (rs1 * rs2)[31:0]` | 
| `mov.i` | R | Move | `rd = rs1` | 
| `addi.i` | I | ADD Immediate | `rd = rs1 + imm` | 
| `xori.i` | I | XOR Immediate | `rd = rs1 ^ imm` |
| `ori.i` | I | OR Immediate | `rd = rs1 OR imm` |
| `andi.i` | I | AND Immediate | `rd = rs1 & imm` | 
| `slli.i` | I | Shift Left Logical Imm| `rd = rs1 << imm[0:4]` |
| `srli.i` | I | Shift Right Logical Imm| `rd = rs1 >> imm[0:4]` |
| `srai.i` | I | Shift Right Arith Imm| `rd = rs1 >> imm[0:4]` |
| `slti.i` | I | Set Less Than Imm | `rd = (rs1 < imm)?1:0` |
| `sltui.i` | I | Set Less Than Imm (U) | `rd = (rs1 < imm)?1:0` |
| `beq.i` | B | Branch == B | ` if(rs1 == rs2) PC += imm` |
| `bne.i` | B | Branch != B | ` if(rs1 != rs2) PC += imm` |
| `blt.i` | B | Branch < B  | `if(rs1 < rs2) PC += imm` |
| `bge.i` | B | Branch ≥ B  | `if(rs1 >= rs2) PC += imm` |
| `lw.i` | I | Load Word | `rd = M[rs1 + imm]` | 
| `lui.i` | U | Load Upper Imm| `rd = imm << 12` | 
| `sw.i` | S | Store Word | `M[rs1 + imm] = rd` | 
| `jal` | UJ | Jump And Link | `rd = PC+4; PC += imm` |
| `jalr`| I | Jump And Link Reg | `rd = PC+4; PC = rs1 + imm`|

## Matrix Instructions
| Instr | Name | Description | 
| ----- | ---- | ----------- | 
| `ld.m` | M | Load Matrix | `md = M[rs1]` | 
| `st.m` | M | Store Matrix | `M[rs1] = md` | 
| `gemm.m` | M | Matrix Multiply | `md = ma @ mb + mc` | 

## Psuedo-instructions
| Instr | Name | Description | Uses |
| ----- | ---- | ----------- | ---- | 
|`li`|Load Immediate|`R[rd] = imm`| `lui.i + addi.i` |
|`mv`|Move|`R[rd] = R[rs1]`| `addi.i` |
|`ret`|Return|`PC = R[1]`| `jalr` |
| `PUSH` | Stack push |`sp = sp - 4; M[sp] <= R[rs1]`| `sub.i + sw.i`|
| `POP` | Stack pop |`sp = sp + 4; R[rs2] <= M[sp]`| `add.i + lw.i` |
| `NOP` | No operation||`addi.i`| 
| `HALT` | halt| |

## Instruction Formats
<table>
    <tr>
        <td></td>
        <td>31 - 25</td>
        <td>24 - 20</td>
        <td>19 - 15</td>
        <td>14 - 12</td>
        <td>11 - 7</td>
        <td>6 - 0</td>
    </tr>
    <tr>
        <td>R</td>
        <td><code>funct7 </code></td>
        <td><code>rs2 </code></td>
        <td><code>rs1 </code></td>
        <td><code>funct3 </code></td>
        <td><code>rd </code></td>
        <td><code>opcode </code></td>
    </tr>
    <tr>
        <td>I</td>
        <td colspan="2"><code>imm[11:0]</code></td>
        <td><code>rs1 </code></td>
        <td><code>funct3 </code></td>
        <td><code>rd </code></td>
        <td><code>opcode </code></td>
    </tr>
        <tr>
        <td>S</td>
        <td><code>imm[11:5]</code></td>
        <td><code>rs2 </code></td>
        <td><code>rs1 </code></td>
        <td><code>funct3 </code></td>
        <td><code>imm[4:0]</code></td>
        <td><code>opcode </code></td>
    </tr>
        </tr>
        <tr>
        <td>B</td>
        <td><code>imm[12|10:5]</code></td>
        <td><code>rs2 </code></td>
        <td><code>rs1 </code></td>
        <td><code>funct3 </code></td>
        <td><code>imm[4:1|11]</code></td>
        <td><code>opcode </code></td>
    </tr>
    <tr>
        <td>U</td>
        <td colspan="4"><code>imm[31:12]</code></td>
        <td><code>rd </code></td>
        <td><code>opcode </code></td>
    </tr>
    <tr>
        <td>UJ</td>
        <td colspan="4"><code>imm[20|10:1|11|19:12]</code></td>
        <td><code>rd </code></td>
        <td><code>opcode </code></td>
    </tr>
</table>
<table>
    <tr>
        <td></td>
        <td>31 - 28</td>
        <td>27 - 24</td>
        <td>23 - 20</td>
        <td>19 - 16</td>
        <td>15 - 7</td>
        <td>6 - 0</td>
    </tr>
    <tr>
        <td>M</td>
        <td><code>rd</code></td>
        <td><code>ra</code></td>
        <td><code>rb</code></td>
        <td><code>rc</code></td>
        <td>reserved</td>
        <td><code>opcode </code></td>
    </tr>
</table>

## Register Allocation
|Register|Name|Use|Saver|
|--------|----|---|-----|
|`x0`|`zero`|Constant 0||
|`x1`|`ra`|Return Address|Caller|
|`x2`|`sp`|Stack Pointer|Callee|
|`x3-x31`||Free||
|`m0`|`mzero`|Zero Matrix||
|`m1-m15`||Free||