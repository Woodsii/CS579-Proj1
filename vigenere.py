# Cracking suspected vigenere ciphertexts - 2 and 18.

import string

def load_ctxts(l, indexes):
    WIDTH = 2

    for i in indexes:
        filename = str(i).zfill(WIDTH)
        ptxtfile = open(f'./ctxts/{filename}.txt')
        ptxt_str = ptxtfile.read()
        l.append(ptxt_str)
    
    return


ctxts = []
load_ctxts(ctxts, [2, 18])

# Ok now to actually crack them.
# im gonna start with monograms
ENGLISH_FREQS = {
    'a': 0.08167, 'b': 0.01492, 'c': 0.02782, 'd': 0.04253, 'e': 0.12702,
    'f': 0.02228, 'g': 0.02015, 'h': 0.06094, 'i': 0.06966, 'j': 0.00015,
    'k': 0.00772, 'l': 0.04025, 'm': 0.02406, 'n': 0.06749, 'o': 0.07507,
    'p': 0.01929, 'q': 0.00095, 'r': 0.05987, 's': 0.06327, 't': 0.09056,
    'u': 0.02758, 'v': 0.00978, 'w': 0.02360, 'x': 0.00150, 'y': 0.01974,
    'z': 0.00074
}

# calculate index of coincidence.
def get_ioc(text):
    n = len(text)

    if n <= 1: 
        return 0
    
    counts = {c: text.count(c) for c in set(text)}
    
    return sum(c * (c - 1) for c in counts.values()) / (n * (n - 1))

# maxamizes IoC to find the most likely key length.
def find_key_length(ciphertext, max_len=20):
    avg_iocs = []
    
    for k in range(1, max_len + 1):
        iocs = []
        for i in range(k):
            column = ciphertext[i::k]
            if len(column) > 1:
                iocs.append(get_ioc(column))
        if iocs:
            avg_iocs.append((k, sum(iocs) / len(iocs)))
            
    avg_iocs.sort(key=lambda x: x[1], reverse=True)
    return avg_iocs[0][0] 

# Using the idea behind a Chi Squared attack I found at this link: 
# https://www.cipherchallenge.org/wp-content/uploads/2020/12/Five-ways-to-crack-a-Vigenere-cipher.pdf
def score_shift(text, shift):
    shifted = ''.join(chr((ord(c) - 97 - shift) % 26 + 97) for c in text)
    chi_sq = 0
    n = len(shifted)

    for char in string.ascii_lowercase:
        observed = shifted.count(char)
        expected = n * ENGLISH_FREQS[char]
        if expected > 0:
            chi_sq += ((observed - expected) ** 2) / expected

    return chi_sq

# minimizes Chi Squared score. 
def find_key(ciphertext, key_len):
    key = ""
    for i in range(key_len):
        column = ciphertext[i::key_len]
        best_shift = min(range(26), key=lambda s: score_shift(column, s))
        key += chr(best_shift + 97)
    return key

# decrypts!
def decrypt(ciphertext, key):
    decrypted = []
    key_len = len(key)
    key_idx = 0
    for char in ciphertext:
        if char.isalpha():
            base = ord('a') if char.islower() else ord('A')
            shift = ord(key[key_idx % key_len].lower()) - ord('a')
            decrypted.append(chr((ord(char) - base - shift) % 26 + base))
            key_idx += 1
        else:
            decrypted.append(char)
    return ''.join(decrypted)

# now lets crackkk
for ctxt in ctxts:
    cleaned_text = ''.join(c.lower() for c in ctxt if c.isalpha())

    key_len = find_key_length(cleaned_text)

    key = find_key(cleaned_text, key_len)

    plaintext = decrypt(ctxt, key)

    print(plaintext)
    print("")
    
