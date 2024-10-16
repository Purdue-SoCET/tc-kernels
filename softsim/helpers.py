
def tobits(data): return [(b >> i) & 1 for i in range(7, -1, -1) for b in data]
def frombits(data): return sum(b << i for i,b in enumerate(data))