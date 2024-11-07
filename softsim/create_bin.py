with open('test_bin', 'wb') as f:
    data = []
    data.append(int('00000000010100000000000010010011', base=2)) # addi x1, x0, 5
    data.append(int('00000000011100000000000100010011', base=2)) # addi x2, x0, 7
    data.append(int('00000000001000001000000110110011', base=2)) # add  x3, x1, x2
    data.append(int('00000000000100000000001000010011', base=2)) # addi x4, x0, 1
    data.append(int('01000000010000000000001010110011', base=2)) # sub  x5, x0, x4
    data.append(int('00000000000100101101001100010011', base=2)) # srli x6, x5, 1
    data.append(int('00000000000100101001001110010011', base=2)) # slli x7, x5, 1
    data.append(int('00000000000100101001001110010011', base=2)) # addi x8, x0, 10
    data.append(int('11111111111111111111111111111111', base=2)) # HALT
    data.append(int('00000000000000000000000000001001', base=2)) # 9

    for d in data:
        f.write(d.to_bytes(4, byteorder='big'))

with open("test_bin", "rb") as f:
    content = f.read()
    print(content)