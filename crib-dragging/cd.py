
# instead of getting the hex representation of the txt file, 
# we directly load the hex that is represented by the ascii of the txt file. 

def load_ctxts(l, indexes):
    WIDTH = 2

    for i in indexes: 
        filename = str(i).zfill(WIDTH)
        ptxtfile = open(f'../ctxts/{filename}.txt')
        ptxt_str = bytes.fromhex(ptxtfile.read())
        l.append(ptxt_str)
    return l

ctxts = []
OTPs = [4, 10, 16, 17]
load_ctxts(ctxts, OTPs)

def drag_crib(crib_str, xor_data, pos = None):
    """
    For each of the words in the FrequentEnglishWordList.csv, 
    drag that crib, see if that generate a valid word
    save the word in a dictionary with the position of that word. 
    """
    crib = crib_str.encode('utf-8')
    
    for i in range(len(xor_data) - len(crib) + 1):

        if pos and pos <= i:
            continue 
        chunk = xor_data[i : i + len(crib)]

        result = bytes([a ^ b for a, b in zip(chunk, crib)])
        
        try:
            # Check if the result is printable ASCII text
            decoded = result.decode('ascii')
            # Filter for common English characters to reduce noise
            if all(32 <= ord(c) <= 126 for c in decoded):
                print(f"--- Dragging crib: '{crib_str}' ---")
                # check if the english word is a real english word.
                print(f"Pos {i}: {decoded}")
                print()
        except:
            pass


# --------------------------------------------------------------

def getKey(M, CTXT):
    M = M.encode('utf-8')

    return bytes([a ^ b for a, b in zip(M, CTXT)])

def removeFogOfWar():
    M = 'in the attention economy, time is bartered'

    k = getKey(M, ctxts[1])

    # now for all of the strings, lets see what we have.
    i = 0
    for ctxt in ctxts: 
        tmp = bytes([a ^ b for a, b in zip(ctxt, k)])
        decoded = tmp.decode('ascii')
        print(f'--- Ciphertext {OTPs[i]} current progress: ---\n{decoded}\n')
        i += 1

# --------------------------------------------------------------
# 0 -> 4
# 1 -> 10 
# 2 -> 16
# 3 -> 17

# Current Strings: 

# hoboken began as lenape homeland. dutch settlers 
# in the attention economy, time is bartered for fl
# the enigma machine, a german rotor cipher, mixed
# chicago rose at a crossroads of water and rail, r

# --------------------------------------------------------------

'''Workspace'''

# removeFogOfWar()

IND1 = 0
IND2 = 1

xored_plaintexts = bytes([a ^ b for a, b in zip(ctxts[IND1], ctxts[IND2])])

cribs = [
    "hoboken began as lenape homeland. dutch settlers "
    ]

for crib in cribs:
    drag_crib(crib, xored_plaintexts, 1)
    print('\n')

# --------------------------------------------------------------

# Code Graveyard

'''
cribs = [
    "in the attention economy, time is a "
    ]

nextWordGuess = []
with open("wordsToTry.txt", "r") as f:
    for line in f:
        nextWordGuess.append(line.strip())

for n in nextWordGuess:
    drag_crib(cribs[0] + n, xored_plaintexts, pos=1)


'''

