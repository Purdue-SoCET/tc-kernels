with open('test_bin', 'wb') as f:
    data = []
    data.append(int('00000000010100000000000010010011', base=2)) # addi x1, x0, 5
    data.append(int('00000000011100000000000100010011', base=2)) # addi x2, x0, 7
    data.append(int('00000000001000001000000110110011', base=2)) # add x3, x1, x2
    data.append(int('11111111111100000100001000010011', base=2)) # xori x4, x0, -1
    data.append(int('00000000000100100101001000010011', base=2)) # srli x4, x4, 1

    for d in data:
        f.write(d.to_bytes(4, byteorder='big'))

with open("test_bin", "rb") as f:
    content = f.read()
    print(content)