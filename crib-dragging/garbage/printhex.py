import binascii

def load_ctxts(l):
    WIDTH = 2

    for i in range(1, 21): 
        filename = str(i).zfill(WIDTH)
        ptxtfile = open(f'../ctxts/{filename}.txt')
        ptxt_str = ptxtfile.read()
        ptxt_bytes = ptxt_str.encode('utf-8')
        l.append(ptxt_bytes)
    
    return

ctxts = []
clusters = [4, 10, 16, 17]
load_ctxts(ctxts)

utf8_text = binascii.unhexlify(ctxts[10]).decode('ascii')