
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

for i in range(1, 20):
    print(f'----Cipher {i}----\n{ctxts[i]}\n')
    input('waiting...')

def shift(byte, sh):

    if 97 > byte or byte > 122: 
        return byte
    
    while sh > 0:
        if byte == 97:
            byte = 122
        else:
            byte -= 1

        sh -= 1
    
    return byte

# manually looking through:
found = [0, 1, 2]

# just gonna try each one and try to find the key.
for i in range(len(ctxts)):
    print(f'\n\n---------Cipher {i}------------') 
    if i in found: continue

    for sh in range(1, 27):
        temp = bytearray()
        for b in ctxts[i]: 
            # 97 to 122.
            temp.append(shift(b, sh))
        
        print(f'--Shift -{sh} --\n{temp}')
    
    input('waiting...')

# 1 -> "hey bob, you've got to stop reusing that one time pad. the students are onto us. let's switch to a stronger cipher.