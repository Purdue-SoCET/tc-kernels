import numpy as np
import argparse
from helpers import tobits, frombits
from opcode import Instruction, Opcode, AluOp, opcodes, rfunct, ifunct, bfunct, alu_funct, branch_funct

# classes

class ControlRegister:
    def __init__(self, start_address: int, stack_pointer: int):
        self.start_address = start_address
        self.stack_pointer = stack_pointer
        
class Instruction:
    
    def __init__(self, op: Opcode):
        self.opcode = op
    
    @staticmethod
    def decode(instruction: bytes) -> Instruction:
        assert len(instruction) == 4, "instructions should be four bytes!"
        bits = tobits(instruction)
        opcode = opcodes[frombits(bits[0:6])]
        instr = Instruction(opcode)
        if opcode is Opcode.RTYPE or opcode is Opcode.MUL:
            instr.rd = frombits(bits[7:11])
            instr.rs1 = frombits(bits[15:19])
            instr.rs2 = frombits(bits[20:24])
            # funct7 ++ funct3
            instr.aluop = rfunct[frombits(bits[25:31] + bits[12:14])]
            return instr
        if opcode is Opcode.ITYPE or opcode is Opcode.LD:
            instr.use_imm = True
            instr.rd = frombits(bits[7:11])
            instr.rs1 = frombits(bits[15:19])
            instr.imm = frombits(bits[20:31])
            instr.aluop = ifunct[frombits(bits[12:14])]
            if instr.aluop is AluOp.SRL and frombits(imm[5:11]) == 0x20: instr.aluop = AluOp.SRA
            return instr
        if opcode is Opcode.ST:
            instr.use_imm = True
            instr.imm = frombits(bits[7:11] + bits[25:31])
            instr.rs1 = frombits(bits[15:19])
            instr.rs2 = frombits(bits[20:24])
            return instr
        if opcode is Opcode.BTYPE:
            instr.use_imm = True
            imm = ([0] + bits[8:11] + bits[25:30] + [bits[7]] + [bits[31]])
            instr.imm = frombits(imm)
            instr.rs1 = frombits(bits[15:19])
            instr.rs2 = frombits(bits[20:24])
            instr.aluop = AluOp.SUB # resolve sign extensions in decode
            instr.branch_cond = bfunct[frombits(bits[12:14])]
            return instr
        if opcode is Opcode.JAL:
            instr.aluop = AluOp.NOP
            instr.rd = frombits(bits[7:11])
            instr.imm = frombits([0] + bits[21:30] + [bits[20]] + bits[12:19] + [bits[31]])
            return instr
        if opcode is Opcode.LUI:
            instr.aluop = AluOp.NOP
            instr.rd = frombits(bits[7:11])
            instr.imm = frombits(bits[12:31])
            return instr
        if opcode is Opcode.GEMM:
            instr.rc = frombits(bits[16:19])
            instr.rb = frombits(bits[20:23])
            instr.ra = frombits(bits[24:27])
            instr.rd = frombits(bits[28:31])
            return instr
        if opcode is Opcode.STM:
            assert False, "we don't have a format for this yet"
        if opcode is Opcode.LDM:
            assert False, "we don't have a format for this yet"
        assert False, f"malformed instruction: f{bits}"
        
class Core:
    def __init__(self, memfile: str, cr: ControlRegister):
        self.memfile = memfile
        with open(self.memfile, "rb") as f:
            self.memory = f.read()
            f.close()
        self.scalar_regs = np.zeros(32)
        self.matrix_regs = np.zeros(32, 8, 8)
    
    def run(self):
        cr = self.load_cr()
        self._run()
        if self.halted: print("exited gracefully.")
        else:
            assert False, "did not halt gracefully"
    
    # read & write a word (byte addressed)
    def memwrite(self, addr: int, data):
        assert addr % 4 == 0, "tried to write to a misaligned address"
        self.memory[addr:addr+3] = data
    def memread(self, addr: int) -> bytes:
        assert addr % 4 == 0, "tried to read from a misaligned address"
        return self.memory[addr:addr+3]
    
    def _run(self, cr: ControlRegister, max_iters=10000):
        # initialize registers
        self.pc = cr.start_address
        self.scalar_regs[2] = cr.stack_pointer
        
        iter = 0
        while iter < max_iters:
            instruction_word = self.memread(self.pc)
            i = Instruction.decode(instruction_word)
            res = self.scalar_alu(i)
            
            # Arithmetic
            if i.opcode is Opcode.RTYPE or Opcode.ITYPE:
                self.scalar_regs[i.rd] = res
                self.pc += 4
                continue
            if i.opcode is Opcode.LUI:
                self.scalar_regs[i.rd] = (self.scalar_regs[i.rd] & ~0xfffff000) | (i.imm << 12)
                self.pc += 4
            
            # Memory
            if i.opcode is Opcode.LD:
                self.scalar_regs[i.rd] = self.memread(res)
            if i.opcode is Opcode.ST:
                self.memwrite(res, self.scalar_regs[i.rs2])
            
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
            
            if i.opcode is Opcode.HALT:
                self.halted = True
                return
        print("reached maximum number of iterations.")
            
    def scalar_alu(self, i):
        op1 = self.scalar_regs[i.rs1]
        op2 =  i.imm if i.use_imm else self.scalar_regs[i.rs2]
        out = alu_funct[i.aluop](op1,op2)
        return out
        
        
        

        
