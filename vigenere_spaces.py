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
load_ctxts(ctxts, [5, 9, 12])

# Ok now to actually crack them.
# im gonna start with monograms
ENGLISH_FREQS = {
    ' ': 17.543860,
    'e': 10.473684,
    't': 7.467303,
    'a': 6.734260,
    'o': 6.190044,
    'i': 5.743952,
    'n': 5.565021,
    's': 5.217052,
    'h': 5.024927,
    'r': 4.936698,
    'd': 3.506895,
    'l': 3.318893,
    'c': 2.293953,
    'u': 2.274163,
    'm': 1.983915,
    'w': 1.945984,
    'f': 1.837141,
    'g': 1.661508,
    'y': 1.627700,
    'p': 1.590595,
    'b': 1.230258,
    'v': 0.806429,
    'k': 0.636568,
    'j': 0.126159,
    'x': 0.123685,
    'q': 0.078334,
    'z': 0.061018
}

ALPHABET = "abcdefghijklmnopqrstuvwxyz "

for k in ENGLISH_FREQS.keys():
    ENGLISH_FREQS[k] = ENGLISH_FREQS[k] / 100

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
    shifted = ''.join(ALPHABET[(ALPHABET.index(c) - shift) % 27] for c in text)
    chi_sq = 0
    n = len(shifted)

    for char in ALPHABET:
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
        best_shift = min(range(27), key=lambda s: score_shift(column, s))
        key += ALPHABET[best_shift]
    return key

# decrypts!
def decrypt(ciphertext, key):
    decrypted = []
    key_len = len(key)
    key_idx = 0

    for char in ciphertext:
        lower_char = char.lower()

        if lower_char in ALPHABET:
            shift = ALPHABET.index(key[key_idx % key_len].lower())
            char_idx = ALPHABET.index(lower_char)
            plain_char = ALPHABET[(char_idx - shift) % 27]
            
            if char.isupper() and plain_char != ' ':
                decrypted.append(plain_char.upper())
            else:
                decrypted.append(plain_char)
                
            key_idx += 1
        else:
            decrypted.append(char)
    return ''.join(decrypted)

# now lets crackkk
for ctxt in ctxts:
        cleaned_text = ''.join(c.lower() for c in ctxt if c.lower() in ALPHABET)

        key_len = find_key_length(cleaned_text)

        key = find_key(cleaned_text, key_len)

        plaintext = decrypt(ctxt, key)
        print(plaintext)
    
