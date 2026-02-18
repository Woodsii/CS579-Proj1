import pandas as pd

# load the cipher texts into bytearray.
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

xored_plaintexts = bytes([a ^ b for a, b in zip(ctxts[3], ctxts[9])])

# load the list of all words, 
dictionary_df = pd.read_csv('./words.csv', header=None)
english_words = set(dictionary_df[0].str.lower())

# and load the list of the 5000 most common english words
cribs_df = pd.read_csv('./FrequentEnglishWordList.csv')
# For a smaller search space: english_words = set(cribs_df['Word'].str.lower())

dic_out = {}

# A simple frequency map for English letters (roughly ordered by popularity)
freq_order = "etaoinshrdlcumwfgypbvkjxqz"

def score_text(text):
    score = 0
    for char in text:
        if char.lower() in freq_order:
            # Higher score for common letters (e is index 0, so 26 points)
            score += (26 - freq_order.index(char.lower()))
        elif char == ' ':
            score += 20 # Spaces are very common and good!
        elif not char.isalnum():
            score -= 10 # Penalize weird symbols
    return score

def drag_crib(crib_str, xor_data):
    """
    For each of the words in the FrequentEnglishWordList.csv, 
    drag that crib, see if that generate a valid word
    save the word in a dictionary with the position of that word. 
    """
    crib = crib_str.encode('utf-8')

    for i in range(len(xor_data) - len(crib) + 1):
        chunk = xor_data[i : i + len(crib)]
        result = bytes([a ^ b for a, b in zip(chunk, crib)])
        
        try:
            decoded = result.decode('ascii')
            if all(32 <= ord(c) <= 126 for c in decoded):
                
                if decoded.lower() in english_words:

                    # ... inside your loop ...
                    try:
                        decoded = result.decode('ascii')
                        # Only keep matches that score high
                        if score_text(decoded) > (len(decoded) * 10): 
                            print(f"Pos {i}: '{crib_str}' reveals -> '{decoded}'")
                            if i not in dic_out:
                                dic_out[i] = []
                            
                            app = f'{crib_str} -> {decoded}'
                            if app not in dic_out[i]:
                                dic_out[i].append(f"{crib_str} -> {decoded}")
                    except:
                        pass
                    
                   

        except UnicodeDecodeError:
            pass

for crib in cribs_df.itertuples():
    drag_crib(crib.Word, xored_plaintexts)

print('Crib Dragging Done!')

def print_visual_reconstruction(dic_out, length=50):
    # Create two empty lines to represent the two messages
    # We use '.' as a placeholder for unknown characters
    msg1 = ['.'] * length
    msg2 = ['.'] * length
    
    print(f"{'POS':<5} | {'CRIB (Guess)':<20} | {'REVEALED (Other Msg)':<20}")
    print("-" * 55)

    # Let's look at the first few successful hits
    for i in sorted(dic_out.keys())[:10]:  # Limit to first 10 for clarity
        for hit in dic_out[i]:
            # The hit string format is "CRIB -> REVEALED"
            crib, revealed = hit.split(' -> ')
            
            print(f"{i:<5} | {crib:<20} | {revealed:<20}")

            # Simple visualization of filling in the blanks
            # (Note: This simple loop overwrites characters, 
            # real reconstruction requires careful merging)
            for idx, char in enumerate(crib):
                if i + idx < length:
                    msg1[i + idx] = char
            
            for idx, char in enumerate(revealed):
                if i + idx < length:
                    msg2[i + idx] = char

    print("\n--- Rough Reconstruction State ---")
    print("Msg 1:", "".join(msg1))
    print("Msg 2:", "".join(msg2))

# Run this with your existing dic_out
print_visual_reconstruction(dic_out)

# Ping: hoboken 
# Pong: in the a