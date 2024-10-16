import struct
import sys

opcode_map = {
    "add.i": 0x33, "sub.i": 0x33, "xor.i": 0x33, "or.i": 0x33, "and.i": 0x33,
    "sll.i": 0x33, "srl.i": 0x33, "sra.i": 0x33, "slt.i": 0x33, "sltu.i": 0x33, "mul.i": 0x33, "mov.i": 0x33,
    "addi.i": 0x13, "xori.i": 0x13, "ori.i": 0x13, "andi.i": 0x13,
    "slli.i": 0x13, "srli.i": 0x13, "srai.i": 0x13, "slti.i": 0x13, "sltui.i": 0x13,
    "ld.i": 0x03, "st.i": 0x23, "beq.i": 0x63, "bne.i": 0x63, "blt.i": 0x63, "bge.i": 0x63,
    "jal": 0x6F, "jalr": 0x67, "lui.i": 0x37,
    "ld.m": 0x43, "st.m": 0x63, "gemm.m": 0x73 #based on the remaining opcodes after riscv-i
}

register_map = {
    "x0": 0, "x1": 1, "x2": 2, "x3": 3, "x4": 4, "x5": 5, "x6": 6, "x7": 7, "x8": 8, "x9": 9,
    "x10": 10, "x11": 11, "x12": 12, "x13": 13, "x14": 14, "x15": 15, "x16": 16, "x17": 17, "x18": 18, "x19": 19,
    "x20": 20, "x21": 21, "x22": 22, "x23": 23, "x24": 24, "x25": 25, "x26": 26, "x27": 27, "x28": 28, "x29": 29,
    "x30": 30, "x31": 31,
    #ask about this
    "m0": 0, "m1": 1, "m2": 2, "m3": 3, "m4": 4, "m5": 5, "m6": 6, "m7": 7, "m8": 8, "m9": 9,
    "m10": 10, "m11": 11, "m12": 12, "m13": 13, "m14": 14, "m15": 15
}

# register_map = {
#     # Integer Registers
#     "x0": 0, "x1": 1, "x2": 2, "x3": 3, "x4": 4, "x5": 5, "x6": 6, "x7": 7, 
#     "x8": 8, "x9": 9, "x10": 10, "x11": 11, "x12": 12, "x13": 13, "x14": 14, 
#     "x15": 15, "x16": 16, "x17": 17, "x18": 18, "x19": 19, "x20": 20, 
#     "x21": 21, "x22": 22, "x23": 23, "x24": 24, "x25": 25, "x26": 26, 
#     "x27": 27, "x28": 28, "x29": 29, "x30": 30, "x31": 31,
    
#     # Matrix Registers (mapped to a different range)
#     "m0": 32, "m1": 33, "m2": 34, "m3": 35, "m4": 36, "m5": 37, "m6": 38, 
#     "m7": 39, "m8": 40, "m9": 41, "m10": 42, "m11": 43, "m12": 44, 
#     "m13": 45, "m14": 46, "m15": 47
# }


def parse_file(filename):
    instructions = []
    with open(filename, 'r') as file:
        for line in file:
            #Removing comments and empty lines
            line = line.split('#')[0].strip()
            if not line:
                continue
            instructions.append(line)
    return instructions

#helper
def get_register_binary(reg):
    return register_map.get(reg, -1)

#R-type
def encode_r_type(opcode, funct3, funct7, rd, rs1, rs2):
    rd_bin = get_register_binary(rd)
    rs1_bin = get_register_binary(rs1)
    rs2_bin = get_register_binary(rs2)
    
    machine_code = (funct7 << 25) | (rs2_bin << 20) | (rs1_bin << 15) | (funct3 << 12) | (rd_bin << 7) | opcode
    return machine_code

#I-type
def encode_i_type(opcode, funct3, rd, rs1, imm):
    rd_bin = get_register_binary(rd)
    rs1_bin = get_register_binary(rs1)
    imm_bin = imm & 0xFFF  # Immediate is 12 bits

    machine_code = (imm_bin << 20) | (rs1_bin << 15) | (funct3 << 12) | (rd_bin << 7) | opcode
    return machine_code

#S-type
def encode_s_type(opcode, funct3, rs1, rs2, imm):
    rs1_bin = get_register_binary(rs1)
    rs2_bin = get_register_binary(rs2)
    imm_bin = imm & 0xFFF  # Immediate- 12 bits

    imm_11_5 = (imm_bin >> 5) & 0x7F 
    imm_4_0 = imm_bin & 0x1F 

    machine_code = (imm_11_5 << 25) | (rs2_bin << 20) | (rs1_bin << 15) | (funct3 << 12) | (imm_4_0 << 7) | opcode
    return machine_code

def encode_b_type(opcode, funct3, rs1, rs2, imm):
    rs1_bin = get_register_binary(rs1)
    rs2_bin = get_register_binary(rs2)
    imm_bin = imm & 0x1FFF  # Immediate- 13 bits

    imm_12 = (imm_bin >> 12) & 0x1
    imm_10_5 = (imm_bin >> 5) & 0x3F
    imm_4_1 = (imm_bin >> 1) & 0xF
    imm_11 = (imm_bin >> 11) & 0x1

    machine_code = (imm_12 << 31) | (imm_10_5 << 25) | (rs2_bin << 20) | (rs1_bin << 15) | (funct3 << 12) | (imm_4_1 << 8) | (imm_11 << 7) | opcode
    return machine_code

def encode_u_type(opcode, rd, imm):
    rd_bin = get_register_binary(rd)
    imm_bin = imm & 0xFFFFF000  # Immediate- 20 bits, shifted left by 12

    machine_code = (imm_bin) | (rd_bin << 7) | opcode
    return machine_code

def encode_uj_type(opcode, rd, imm):
    rd_bin = get_register_binary(rd)
    imm_bin = imm & 0xFFFFF  # Immediate-20 bits (signed)

    imm_20 = (imm_bin >> 20) & 0x1
    imm_10_1 = (imm_bin >> 1) & 0x3FF
    imm_11 = (imm_bin >> 11) & 0x1 
    imm_19_12 = (imm_bin >> 12) & 0xFF 

    machine_code = (imm_20 << 31) | (imm_19_12 << 12) | (imm_11 << 20) | (imm_10_1 << 21) | (rd_bin << 7) | opcode
    return machine_code

def encode_m_type(opcode, rd, ra, rb, rc):
    rd_bin = get_register_binary(rd)
    ra_bin = get_register_binary(ra)
    rb_bin = get_register_binary(rb)
    rc_bin = get_register_binary(rc)

    machine_code = (rd_bin << 28) | (ra_bin << 24) | (rb_bin << 20) | (rc_bin << 16) | opcode
    return machine_code

def handle_instruction(instruction):
    parts = instruction.split()
    instr = parts[0]

    if instr in ["add.i", "sub.i", "xor.i", "or.i", "and.i", "sll.i", "srl.i", "sra.i", "slt.i", "sltu.i", "mul.i", "mov.i"]:
        rd, rs1, rs2 = parts[1].strip(','), parts[2].strip(','), parts[3]
        funct3, funct7 = 0, 0 
        if instr == "add.i": funct3, funct7 = 0x0, 0x00
        elif instr == "sub.i": funct3, funct7 = 0x0, 0x20
        elif instr == "xor.i": funct3, funct7 = 0x4, 0x00
        elif instr == "or.i": funct3, funct7 = 0x6, 0x00
        elif instr == "and.i": funct3, funct7 = 0x7, 0x00
        elif instr == "sll.i": funct3, funct7 = 0x1, 0x00
        elif instr == "srl.i": funct3, funct7 = 0x5, 0x00
        elif instr == "sra.i": funct3, funct7 = 0x5, 0x20
        elif instr == "slt.i": funct3, funct7 = 0x2, 0x00
        elif instr == "sltu.i": funct3, funct7 = 0x3, 0x00
        elif instr == "mul.i": funct3, funct7 = 0x0, 0x01
        elif instr == "mov.i": funct3, funct7 = 0x0, 0x00
        return [encode_r_type(opcode_map[instr], funct3, funct7, rd, rs1, rs2)]

    elif instr in ["addi.i", "xori.i", "ori.i", "andi.i", "slli.i", "srli.i", "srai.i", "slti.i", "sltui.i", "ld.i", "jalr"]:
        rd, rs1, imm = parts[1].strip(','), parts[2].strip(','), int(parts[3])
        funct3 = 0 
        if instr == "addi.i": funct3 = 0x0
        elif instr == "xori.i": funct3 = 0x4
        elif instr == "ori.i": funct3 = 0x6
        elif instr == "andi.i": funct3 = 0x7
        elif instr == "slli.i": funct3 = 0x1
        elif instr == "srli.i": funct3 = 0x5
        elif instr == "srai.i": funct3 = 0x5
        elif instr == "slti.i": funct3 = 0x2
        elif instr == "sltui.i": funct3 = 0x3
        elif instr == "ld.i": funct3 = 0x2
        elif instr == "jalr": funct3 = 0x0
        return [encode_i_type(opcode_map[instr], funct3, rd, rs1, imm)]

    elif instr == "st.i":
        rs1, rs2, imm = parts[1].strip(','), parts[2].strip(','), int(parts[3])
        funct3 = 0x2
        return [encode_s_type(opcode_map[instr], funct3, rs1, rs2, imm)]

    elif instr in ["beq.i", "bne.i", "blt.i", "bge.i"]:
        rs1, rs2, imm = parts[1].strip(','), parts[2].strip(','), int(parts[3])
        funct3 = 0
        if instr == "beq.i": funct3 = 0x0
        elif instr == "bne.i": funct3 = 0x1
        elif instr == "blt.i": funct3 = 0x4
        elif instr == "bge.i": funct3 = 0x5
        return [encode_b_type(opcode_map[instr], funct3, rs1, rs2, imm)]

    
    elif instr == "lui.i":
        rd, imm = parts[1].strip(','), int(parts[2])
        return [encode_u_type(opcode_map[instr], rd, imm)]

    elif instr == "jal":
        rd, imm = parts[1].strip(','), int(parts[2])
        return [encode_uj_type(opcode_map[instr], rd, imm)]

    elif instr in ["ld.m", "st.m", "gemm.m"]:
        rd, ra, rb, rc = parts[1].strip(','), parts[2].strip(','), parts[3].strip(','), parts[4]
        return [encode_m_type(opcode_map[instr], rd, ra, rb, rc)]

    return [0]

def assemble_instructions(instructions):
    machine_codes = []
    for instr in instructions:
        codes = handle_instruction(instr)
        machine_codes.extend(codes)
    return machine_codes

def write_machine_code(filename, machine_codes):
    with open(filename, 'wb') as f:
        for code in machine_codes:
            f.write(struct.pack('<I', code)) #because it needs to be raw bytes and not integers

def assemble_file(input_file, output_file):
    instructions = parse_file(input_file)
    machine_codes = assemble_instructions(instructions)
    write_machine_code(output_file, machine_codes)
    print(f"Machine code written to {output_file}.")

if __name__ == "__main__":
    input_file = sys.argv[1]
    output_file = sys.argv[2]

    assemble_file(input_file, output_file)