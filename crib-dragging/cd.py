
# instead of getting the hex representation of the txt file, 
# we directly load the hex.
def load_ctxts(l, indexes):
    WIDTH = 2

    for i in indexes: 
        filename = str(i).zfill(WIDTH)
        ptxtfile = open(f'../ctxts/{filename}.txt')
        ptxt_str = bytes.fromhex(ptxtfile.read())
        l.append(ptxt_str)
    return l

ctxts = []
load_ctxts(ctxts, [4, 10, 16, 17])

xored_plaintexts = bytes([a ^ b for a, b in zip(ctxts[0], ctxts[1])])

# load the shit

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

cribs = [
    "in the attention economy, time is a "
    ]

# hoboken began as lenape homeland. 
# in the attention economy, time is the most expensive currenc

'''
nextWordGuess = []
with open("wordsToTry.txt", "r") as f:
    for line in f:
        nextWordGuess.append(line.strip())

for n in nextWordGuess:
    drag_crib(cribs[0] + n, xored_plaintexts, pos=1)

for crib in cribs:
    drag_crib(crib, xored_plaintexts, 1)
    print('\n')
'''

