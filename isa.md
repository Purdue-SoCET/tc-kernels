# ISA
## Data types
| type | suffix | format | description
| ---- | ------ | ------ | -----------
| matrix | `.m` | 4x4 array of FP16 | The matrix data type for the systolic array
| int | `.i` | 32 bit signed integer | 

## Integer Instructions
| Instr | Type | Name | Description | Opcode |
| ----- | ---- | ---- | ----------- | ------ |
| `add.i` | R | ADD | `rd = rs1 + rs2` | `0b0110011` |
| `sub.i` | R | SUB | `rd = rs1 - rs2` | `0b0110011` |
| `xor.i` | R | XOR | `rd = rs1 ^ rs2` |`0b0110011` |
| `or.i` | R | OR | `rd = rs1 OR rs2` |`0b0110011` |
| `and.i` | R | AND | `rd = rs1 & rs2` | `0b0110011` |
| `sll.i` | R | Shift Left Logical | `rd = rs1 << rs2` |`0b0110011` |
| `srl.i` | R | Shift Right Logical | `rd = rs1 >> rs2` |`0b0110011` |
| `sra.i` | R | Shift Right Arith | `rd = rs1 >> rs2` |`0b0110011` |
| `slt.i` | R | Set Less Than | `rd = (rs1 < rs2)?1:0` |`0b0110011` |
| `sltu.i` | R | Set Less Than (U) | `rd = (rs1 < rs2)?1:0` |`0b0110011` |
| `mul.i` | R | Multiply | `rd = (rs1 * rs2)[31:0]` | `0b0110011` |
| `mov.i` | R | Move | `rd = rs1` !NOT IN RISCV SPEC! | `0b0110011` |
| `addi.i` | I | ADD Immediate | `rd = rs1 + imm` | `0b0010011` |
| `xori.i` | I | XOR Immediate | `rd = rs1 ^ imm` |`0b0010011` |
| `ori.i` | I | OR Immediate | `rd = rs1 OR imm` |`0b0010011` |
| `andi.i` | I | AND Immediate | `rd = rs1 & imm` | `0b0010011` |
| `slli.i` | I | Shift Left Logical Imm| `rd = rs1 << imm[0:4]` | `0b0010011` |
| `srli.i` | I | Shift Right Logical Imm| `rd = rs1 >> imm[0:4]` |`0b0010011` |
| `srai.i` | I | Shift Right Arith Imm| `rd = rs1 >> imm[0:4]` |`0b0010011` |
| `slti.i` | I | Set Less Than Imm | `rd = (rs1 < imm)?1:0` |`0b0010011` |
| `sltui.i` | I | Set Less Than Imm (U) | `rd = (rs1 < imm)?1:0` |`0b0010011` |
| `beq.i` | B | Branch == B | ` if(rs1 == rs2) PC += imm` |`0b1100011` |
| `bne.i` | B | Branch != B | ` if(rs1 != rs2) PC += imm` |`0b1100011` |
| `blt.i` | B | Branch < B  | `if(rs1 < rs2) PC += imm` |`0b1100011` |
| `bge.i` | B | Branch ≥ B  | `if(rs1 >= rs2) PC += imm` |`0b1100011` |
| `lw.i` | I | Load Word | `rd = M[rs1 + imm]` | `0b0000011` |
| `lui.i` | U | Load Upper Imm| `rd = imm << 12` | `0b0110111` |
| `sw.i` | S | Store Word | `M[rs1 + imm] = rd` | `0b0100011` |
| `jal` | UJ | Jump And Link | `rd = PC+4; PC += imm` |`0b1101111` |
| `jalr`| I | Jump And Link Reg | `rd = PC+4; PC = rs1 + imm`|`0b1100111` |

## Matrix Instructions
| Instr | Type | Name | Description | Opcode |
| ----- |---- | ---- |----------- | ------ |
| `ld.m` | M | Load Matrix | `md = M[rs1 + imm]` | `0b1000111` |
| `st.m` | M | Store Matrix | `M[rs1 + imm] = md` | `0b1010111` |
| `gemm.m` | GEMM | Matrix Multiply | `md = ma @ mb + mc` | `0b1110111` |

## Psuedo-instructions
| Instr | Name | Description | Uses |
| ----- | ---- | ----------- | ---- | 
|`LI`|Load Immediate|`R[rd] = imm`| `lui.i + addi.i` |
|`MV`|Move|`R[rd] = R[rs1]`| `addi.i` |
|`RET`|Return|`PC = R[1]`| `jalr` |
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
        <td>GEMM</td>
        <td><code>rd</code></td>
        <td><code>ra</code></td>
        <td><code>rb</code></td>
        <td><code>rc</code></td>
        <td>reserved</td>
        <td><code>opcode </code></td>
        <td><strong>meaningless register names</strong></td>
    </tr>
        <tr>
        <td></td>
        <td>31 - 28</td>
        <td>27 - 23</td>
        <td>22 - 18</td>
        <td>17 - 7</td>
        <td>6 - 0</td>
    </tr>
    <tr>
        <td>M</td>
        <td><code>rd</code></td>
        <td><code>rs1</code></td>
        <td><code>stride</code></td>
        <td><code>Imm[10:0]</code></td>
        <td><code>opcode</code></td>
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