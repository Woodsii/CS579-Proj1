import os
from collections import Counter
from tabulate import tabulate

# lets start by loading in all the files to a list of bytearrays

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

'''

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
'''

# Subsitution Ciphers
prob_sub = [1, 4, 17]
maybe_sub = [6, 8, 11, 14]

# Anything from 0x00 to 0x0F is control and I think the cipher ignores them. 
# Frequency of characters time! 

freqs = [dict(Counter(ctxts[i])) for i in range(20)]

# alphanumeric only - who cares about special characters?
def print_byte_counts(list_of_dicts, items=[i for i in range(0, 20)]):
    for i, d in enumerate(list_of_dicts):
        if i not in items: continue
        print(f"--- Item {i+1} ---")
        for byte_val, count in sorted(d.items(), key=lambda x: x[1], reverse=True):
            if 48 <= byte_val <= 57 or 97 <= byte_val <= 122:
                char_repr = f"'{chr(byte_val)}'"
            else:
                continue
            
            print(f"  Byte {byte_val:<3} (0x{byte_val:02X}) | {char_repr:<13} : {count} occurrences")
        print()

# brute forcing suspected shift ciphers with freq analysis.

# print_byte_counts(freqs, prob_sub)

# Keyspace is some permuation of the alphabet
# No numerical values though!
# two pointer through the ctxts frequency and the ctxt itself. 
# allow for going back
def break_subsitution_cipher(ctxt, ctxt_freq): 
    # Standard English frequencies (most common to least common)
    letters = [
        'e', 't', 'a', 'o', 'i', 'n', 's', 'r', 'h', 'd', 
        'l', 'u', 'c', 'm', 'f', 'y', 'w', 'g', 'p', 'b', 
        'v', 'k', 'x', 'q', 'j', 'z'
    ]

    # Clean and sort the ciphertext frequencies (only alpha)
    # We want a list of tuples like [('q', 50), ('z', 42), ...]
    sorted_ctxt_chars = sorted(
        [(chr(k).lower(), v) for k, v in ctxt_freq.items() if chr(k).isalpha()],
        key=lambda x: x[1], 
        reverse=True
    )

    # Convert ctxt to list for easy manipulation (strings are immutable)
    working_text = str(ctxt.decode("utf-8").lower())
    mapping = {} # To keep track of our discoveries: {cipher_char: plain_char}
    
    # ok prompt the user with hey these are the most likely options for these chars
    # but what do you want to be what.
    while letters != []:
        os.system('clear')

        print(f'\n-- Working Decryption --\n{working_text}')

        
        print(tabulate(sorted_ctxt_chars, headers=['Character', 'Frequency']))


        to_swap = input('\nWhat character do you want to swap? ')
        if to_swap not in letters: 
            print(f'{to_swap} is not a valid choice!\n')
            continue
            
        replacement = input('What character do you want to change it to? ')
        if replacement in mapping.values():
            print(f'{to_swap} is already in the working text!\n')
            continue
            
        mapping[to_swap] = replacement
        working_text = working_text.replace(to_swap, replacement.upper())

        letters.remove(to_swap)

# Decimal Encoding
# Lets start by trying to grab every 2 dec.

dec_encoded_indexes = [3, 6, 8, 11, 13, 14, 19, 20]
dec_endoded = []

# converts int -> character
for ctxt_index in dec_encoded_indexes: 
    tmp = []

    for i in range(0, len(ctxts[ctxt_index - 1])):
        tmp.append(chr(ctxts[ctxt_index - 1][i]))

    dec_endoded.append(tmp)

# Hex Encoding: 
# Step one, get it into hexadecimal.


hex_encoded_indexes = [4, 10, 16, 17]

# just dealing with 4 rn: 

ptxtfile = open(f'./ctxts/04.txt')
ptxt_str = ptxtfile.read()
ciphertext_bytes = bytes.fromhex(ptxt_str)
print(ptxt_str)

