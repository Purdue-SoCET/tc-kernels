import numpy as np
import argparse
from helpers import tobits, frombits
from opcode import Opcode, AluOp, opcodes, rfunct, ifunct, bfunct, alu_funct, branch_funct

# classes

class ControlRegister:
    def __init__(self, start_address: int, stack_pointer: int):
        self.start_address = start_address
        self.stack_pointer = stack_pointer
        
class Instruction:
    
    def __init__(self, op: Opcode):
        self.opcode = op
        self.aluop = None
        self.rs1 = None
        self.rs2 = None
        self.ra = None
        self.rb = None
        self.rc = None
        self.rd = None
        self.imm = None
        self.use_imm = False
    
    @staticmethod
    def decode(instruction: bytes):
        assert len(instruction) == 4, "instructions should be four bytes!"
        bits = tobits(instruction)
        # print(bits)
        def bit_range(a, b = None):
            if b is None: b = a
            return bits[a: b + 1]

        # print("Bits: ", bits)
        opcode = opcodes[frombits(bit_range(0,6))]
        instr = Instruction(opcode)
        if opcode is Opcode.HALT:
            return instr
        if opcode is Opcode.RTYPE or opcode is Opcode.MUL:
            instr.rd = frombits(bit_range(7,11))
            instr.rs1 = frombits(bit_range(15,19))
            instr.rs2 = frombits(bit_range(20,24))
            # funct7 ++ funct3
            instr.aluop = rfunct[frombits(bit_range(25,31) + bit_range(12,14))]
            return instr
        if opcode is Opcode.ITYPE or opcode is Opcode.LW:
            instr.use_imm = True
            instr.rd = frombits(bit_range(7,11))
            instr.rs1 = frombits(bit_range(15,19))
            instr.imm = frombits(bit_range(20,31), signed = True)
            instr.aluop = ifunct[frombits(bit_range(12,14))]
            # if instr.aluop is AluOp.SRL and frombits(imm[5:11]) == 0x20: instr.aluop = AluOp.SRA
            return instr
        if opcode is Opcode.SW:
            instr.use_imm = True
            instr.imm = frombits(bit_range(7, 11) + bit_range(25,31))
            instr.rs1 = frombits(bit_range(15,19))
            instr.rs2 = frombits(bit_range(20,24))
            instr.aluop = ifunct[frombits(bit_range(12,14))]
            return instr
        if opcode is Opcode.BTYPE:
            instr.use_imm = False
            imm = ([0] + bit_range(8,11) + bit_range(25,30) + [bits[7]] + [bits[31]])
            instr.imm = frombits(imm, signed = True)
            instr.rs1 = frombits(bit_range(15,19))
            instr.rs2 = frombits(bit_range(20,24))
            instr.aluop = AluOp.SUB # resolve sign extensions in decode
            instr.branch_cond = bfunct[frombits(bit_range(12,14))]
            return instr
        if opcode is Opcode.JAL:
            instr.aluop = AluOp.NOP
            instr.rd = frombits(bit_range(7,11))
            instr.imm = frombits([0] + bit_range(21,30) + [bits[20]] + bit_range(12,19) + [bits[31]])
            return instr
        if opcode is Opcode.LUI:
            instr.aluop = AluOp.NOP
            instr.rd = frombits(bit_range(7,11))
            instr.imm = frombits(bit_range(12,31))
            return instr
        if opcode is Opcode.GEMM:
            instr.rc = frombits(bit_range(16,19))
            instr.rb = frombits(bit_range(20,23))
            instr.ra = frombits(bit_range(24,27))
            instr.rd = frombits(bit_range(28,31))
            instr.aluop = AluOp.NOP
            return instr
        if opcode is Opcode.STM or opcode is Opcode.LDM:
            instr.use_imm = True
            instr.rd = frombits(bit_range(28, 31))
            instr.rs1 = frombits(bit_range(23, 27))
            instr.stride = frombits(bit_range(18, 22))
            instr.imm = frombits(bit_range(7, 17))
            instr.aluop = AluOp.ADD
            return instr
        assert False, f"malformed instruction: f{bits}"

    def print_instr(self):
        st = "- "
        if self.opcode is Opcode.HALT: print(st + "HALT"); return
        if self.aluop: 
            if self.opcode is Opcode.BTYPE:
                st += str(self.branch_cond)[9:].lower()
            else:
                if self.opcode in {Opcode.SW, Opcode.LW, Opcode.LUI, 
                                   Opcode.LDM, Opcode.STM, Opcode.GEMM}:
                    st += str(self.opcode)[7:].ljust(4, ' ').lower()
                else:
                    st += (str(self.aluop).lower()[6:] + 'i'*self.use_imm).ljust(4, ' ')
        var = ", x"
        if self.opcode in {Opcode.STM, Opcode.LDM, Opcode.GEMM}: 
            var = ", m"
        if self.rd is not None:     st += var[1:] + str(self.rd)
        if self.rs1 is not None and self.opcode not in {Opcode.SW, Opcode.LW}: st += ", x" + str(self.rs1) 
        if self.rs2 is not None:    st += var + str(self.rs2) 
        if self.ra is not None:     st += var + str(self.ra) 
        if self.rb is not None:     st += var + str(self.rb)
        if self.rc is not None:     st += var + str(self.rc) 
        if self.imm is not None:
            if self.opcode not in {Opcode.SW, Opcode.LW, Opcode.LDM, Opcode.STM}:
                st += var[:-1] + str(self.imm)
            else:
                st += f", {self.imm}(x{self.rs1})"
        if self.opcode is Opcode.BTYPE: st = st[0:5] + ' ' + st[6:]
        if self.opcode is Opcode.SW: st = st[0:6] + st[7:]
        print(st)

        
class Core:
    def __init__(self, memfile: str, cr: ControlRegister):
        self.memfile = memfile
        with open(self.memfile, "rb") as f:
            self.memory = f.read()
            f.close()
        self.scalar_regs = np.zeros(32, dtype=np.int32)
        self.matrix_regs = np.zeros((16, 4, 4),  dtype=np.float16)
        self.cr = cr
    
    def run(self):
        cr = self.cr
        self._run(cr)
        if self.halted: print("exited gracefully.")
        else:
            assert False, "did not halt gracefully"
    
    # read & write a word (byte addressed)
    def memwrite(self, addr: int, data):
        assert addr % 4 == 0, "tried to write to a misaligned address"
        self.memory = self.memory[0:addr] + data + self.memory[addr+4:]

    def memread(self, addr: int) -> bytes:
        assert addr % 4 == 0, "tried to read from a misaligned address"
        return self.memory[addr:addr+4]

    
    def _run(self, cr: ControlRegister, max_iters=100):
        # initialize registers
        self.pc = cr.start_address
        self.scalar_regs[2] = cr.stack_pointer
        
        iter = 0
        while iter < max_iters:
            iter += 1

            instruction_word = self.memread(self.pc)
            instruction_word = instruction_word[::-1]
            i = Instruction.decode(instruction_word)

            i.print_instr()

            if i.opcode is Opcode.HALT:
                self.halted = True
                print("Program halted")
                return
            res = np.int32(self.scalar_alu(i))
            
            # Arithmetic
            if i.opcode is Opcode.RTYPE or i.opcode is Opcode.ITYPE:
                self.scalar_regs[i.rd] = res
                self.pc += 4
                continue
            if i.opcode is Opcode.LUI:
                self.scalar_regs[i.rd] = np.int32(np.uint32(i.imm) << 12)
                self.pc += 4
            
            # Memory
            if i.opcode is Opcode.LW:
                value = np.int32(int.from_bytes(self.memread(res), byteorder='little'))
                self.scalar_regs[i.rd] = value
                self.pc += 4
            if i.opcode is Opcode.SW:
                self.memwrite(res, self.scalar_regs[i.rs2])
                self.pc += 4
            
            # Control Flow
            if i.opcode is Opcode.BTYPE:
                if branch_funct[i.branch_cond](res): self.pc += (i.imm << 1) # check sign extension
                else: self.pc += 4
                continue
            
            if i.opcode is Opcode.JAL:
                self.scalar_regs[2] = self.pc + 4
                self.pc += i.imm << 1
                continue
        
            if i.opcode is Opcode.JALR:
                self.scalar_regs[2] = self.pc + 4
                self.pc += self.scalar_regs[i.rs1] + i.imm
                continue

            #Matrix
            if i.opcode is Opcode.LDM:
                nums = np.array((), dtype = np.float16)
                content = self.memory[res:res+32]
                for c in range(len(content) // 2):
                    fl = np.frombuffer(content[2*c:2*c+2], dtype=np.float16)[0]
                    nums = np.append(nums, fl)
                nums = nums.reshape((4, 4))
                # print(nums)
                self.matrix_regs[i.rd] = nums
                self.pc += 4

            if i.opcode is Opcode.STM:
                nums = self.matrix_regs[i.rd]
                assert nums.shape == (4, 4), "Must be 4x4 matrix"
                assert nums.dtype == np.float16, "Must use fp16"
                nums.flatten()
                out = None
                for n in nums:
                    if out is None: out = n.tobytes()
                    else:           out += n.tobytes()
                self.memory = self.memory[:res] + out + self.memory[res+32:]
                self.pc += 4

            if i.opcode is Opcode.GEMM:
                W = self.matrix_regs[i.ra]
                I = self.matrix_regs[i.rb]
                A = self.matrix_regs[i.rc]
                self.matrix_regs[i.rd] = np.matmul(W, I) + A
                self.pc += 4
        print("reached maximum number of iterations.")
            
    def scalar_alu(self, i):
        op1 = self.scalar_regs[i.rs1]
        op2 =  i.imm if i.use_imm else self.scalar_regs[i.rs2]
        out = alu_funct[i.aluop](op1,op2)
        return out

    def print_scalar_regs(self):
        print("Scalar Registers: ")
        s = ""
        for i, n in enumerate(self.scalar_regs):
            s += f"x{str(i).zfill(2)}| {str(np.int32(n)).ljust(10, ' ')}     "
            if not (i+1) % 4:
                print(s)
                s = ""
        print()

    def print_matrix_regs(self):
        print("Matrix Registers: ")
        for i, m in enumerate(self.matrix_regs):
            if np.allclose(np.zeros(np.shape(m)), m): m_str = "[0]" 
            else: m_str = "\n" + str(m)
            print(f"m{str(i).zfill(2)}| {m_str}")
        print()

    def print_data_memory(self):
        DATA_START = 0x200
        i = DATA_START
        print("Data memory: ")
        print("Addr.    int32", 9*" ", "fp16 [31:16]", 4*" ", "fp16 [15:0]")
        while (i < len(self.memory)):
            as_int = str(np.frombuffer(self.memory[i:i+4], dtype=np.int32)[0])
            f1 = str(np.frombuffer(self.memory[i:i+2], dtype=np.float16)[0])
            f2 = str(np.frombuffer(self.memory[i+2:i+4], dtype=np.float16)[0])
            print(hex(i), "| ", as_int.ljust(15, ' '), f1.ljust(15, ' '), f2.ljust(15, ' '))
            i += 4
        print()
        
if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--file', type=str, required=True)
    args=parser.parse_args()
    filename = args.file
    print("Running file", filename)
    cr = ControlRegister(0, 0)
    core = Core(filename, cr)
    core.run()
    core.print_scalar_regs()
    # core.matrix_regs = np.random.random((16, 4, 4)) * 10
    core.print_matrix_regs()
    core.print_data_memory()

