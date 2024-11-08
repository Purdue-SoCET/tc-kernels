
def tobits(data, bit_len = 8): 
    bits = []
    for b in data:
        for i in range(bit_len - 1, -1, -1):
            bits.append((b >> i) & 1)
    bits.reverse()
    return bits

def frombits(data, signed = False):
    if data[-1] and signed: return -1 * frombits([int(not n) for n in data]) - 1
    else: return sum(b << i for i,b in enumerate(data))
   