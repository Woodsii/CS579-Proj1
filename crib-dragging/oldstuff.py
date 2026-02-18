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
load_ctxts(ctxts)

xored_plaintexts = bytes([a ^ b for a, b in zip(ctxts[4], ctxts[8])])

# load the shit

def drag_crib(crib_str, xor_data, pos = None):
    """
    For each of the words in the FrequentEnglishWordList.csv, 
    drag that crib, see if that generate a valid word
    save the word in a dictionary with the position of that word. 
    """
    crib = crib_str.encode('utf-8')
    print(f"--- Dragging crib: '{crib_str}' ---")
    
    for i in range(len(xor_data) - len(crib) + 1):

        if pos and pos >= i:
            continue 
        chunk = xor_data[i : i + len(crib)]

        result = bytes([a ^ b for a, b in zip(chunk, crib)])
        
        try:
            # Check if the result is printable ASCII text
            decoded = result.decode('ascii')
            # Filter for common English characters to reduce noise
            if all(32 <= ord(c) <= 126 for c in decoded):
                
                # check if the english word is a real english word.
                print(f"Pos {i}: {decoded}")
        except:
            pass

common_cribs = [" and "] 

for crib in common_cribs:
    drag_crib(crib, xored_plaintexts)