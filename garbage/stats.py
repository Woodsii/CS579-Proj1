def load_ctxts(l):
    WIDTH = 2

    for i in range(1, 21): 
        filename = str(i).zfill(WIDTH)
        ptxtfile = open(f'./ctxts/{filename}.txt')
        ptxt_str = ptxtfile.read()
        ptxt_bytes = ptxt_str.encode('utf-8')
        l.append(ptxt_bytes)
    
    return

ctxts = []
load_ctxts(ctxts)

import math
from collections import Counter

def calculate_stats(data_bytes):
    n = len(data_bytes)
    if n < 2: return 0, 0
    
    counts = Counter(data_bytes)
    
    # 1. Entropy
    entropy = 0
    for count in counts.values():
        p_x = count / n
        entropy -= p_x * math.log2(p_x)
        
    # 2. Index of Coincidence
    ic_sum = sum(count * (count - 1) for count in counts.values())
    ic = ic_sum / (n * (n - 1))
    
    return entropy, ic

print(f"{'Entropy':<10} | {'IC':<10}")
print("-" * 22)
for data in ctxts:
    ent, ic = calculate_stats(data)
    print(f"{ent:<10.4f} | {ic:<10.4f}")

