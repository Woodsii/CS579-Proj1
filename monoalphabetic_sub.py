import string

def load_ctxts(l, indexes):
    WIDTH = 2

    for i in indexes:
        filename = str(i).zfill(WIDTH)
        ptxtfile = open(f'./ctxts/{filename}.txt')
        ptxt_str = ptxtfile.read()
        l.append(ptxt_str)
    
    return l


ctxts = []
CNUMS = [7, 15]
load_ctxts(ctxts, CNUMS)

# good old fashioned freq. analaysis
# injecting space into this -- im just assuming that it's got the highest probability of appearing?
ENGLISH_FREQS = {
    'a': 0.08167, 'b': 0.01492, 'c': 0.02782, 'd': 0.04253, 'e': 0.12702,
    'f': 0.02228, 'g': 0.02015, 'h': 0.06094, 'i': 0.06966, 'j': 0.00015,
    'k': 0.00772, 'l': 0.04025, 'm': 0.02406, 'n': 0.06749, 'o': 0.07507,
    'p': 0.01929, 'q': 0.00095, 'r': 0.05987, 's': 0.06327, 't': 0.09056,
    'u': 0.02758, 'v': 0.00978, 'w': 0.02360, 'x': 0.00150, 'y': 0.01974,
    'z': 0.00074, ' ': 1
}

IND = 0
ctxt = ctxts[IND]

# lets construct a frequency map of letters in the text:

ctxt_freqs = {}
l = len(ctxt)

for c in ctxt:
    if c == '\n': continue
    if c not in ctxt_freqs.keys():
        ctxt_freqs[c] = 0
    ctxt_freqs[c] += (1 / l)

# ok with that out of the way, lets sort each dictionary and print the top side by side. 

sorted_ctxt_freqs = sorted(ctxt_freqs.items(), key=lambda item: item[1])
sorted_ctxt_freqs = dict(sorted_ctxt_freqs)

sorted_english_freqs = sorted(ENGLISH_FREQS.items(), key=lambda item: item[1])
sorted_english_freqs = dict(sorted_english_freqs)

# ok with them sorted, lets grab the matches. 

key_map = {
        'a': 'o', 'b': 's', 'c': 'z', 'd': 'a', 'e': 'k', 'f': 'p', 
        'g': 'u', 'h': 'r', 'i': 'l', 'j': ' ', 'k': 'g', 'l': 'c', 
        'm': 'd', 'n': 'm', 'o': 'y', 'p': 'w', 'q': 'v', 'r': 'e', 
        's': 'b', 't': 'i', 'u': 'n', 'v': 'h', 'w': 'j', 'x': 't', 
        'y': 'f', 'z': 'x', ' ': 'q'
    }

for i in range(len(ctxts)):
    plaintext = ""
    for char in ctxts[i]:        
        if char in key_map:
            # Swap the character based on our map
            plaintext += key_map[char]
        else:
            # Pass punctuation, newlines, and numbers through unchanged
            plaintext += char
            
    print(f'Ciphertext {CNUMS[i]}:\n{plaintext}')
    
