
def tobits(data): 
    bits = []
    for b in data:
        for i in range(7, -1, -1):
            bits.append((b >> i) & 1)
    bits.reverse()
    return bits

def frombits(data): return sum(b << i for i,b in enumerate(data))