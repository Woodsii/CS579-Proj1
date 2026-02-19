import csv
import string

ret = []

def find_matching_words(csv_file_path):
    # The exact XOR differences at indices 8, 9, 10, and 11
    # These represent (P1 ^ P2) at those specific positions
    xor_values = [6, 20, 6, 23, 13, 82, 22, 1, 84]
    
    # The only allowed characters in the messages (lowercase a-z + space)
    valid_chars = set(string.ascii_lowercase + ' ')
    
    candidates = []
    
    # Open the dictionary CSV. 
    # (Note: Change 'utf-8' or the delimiter if your CSV requires it)
    try:
        with open(csv_file_path, mode='r', encoding='utf-8') as file:
            reader = csv.reader(file)
            
            for row in reader:
                if not row:
                    continue
                    
                # Assuming the dictionary words are in the first column
                word = row[1].strip().lower()
                
                # We need words that start with 'a' and are at least 5 letters 
                # long to cover the 'a' plus the 4 unknown XOR positions.
                if len(word) >= 5 and word.startswith('a'):
                    is_valid_match = True
                    p1_derived_chars = []
                    
                    # Test the next 4 characters of the candidate word
                    for i in range(4):
                        # Get the 2nd, 3rd, 4th, and 5th characters of the word
                        p2_char = word[i + 1] 
                        
                        # Mathematically force the P1 character: P1 = P2 ^ (P1 ^ P2)
                        p1_char_val = ord(p2_char) ^ xor_values[i]
                        p1_char = chr(p1_char_val)
                        
                        # If the resulting P1 character isn't a lowercase letter 
                        # or a space, this dictionary word is mathematically impossible.
                        if p1_char not in valid_chars:
                            is_valid_match = False
                            break
                        
                        p1_derived_chars.append(p1_char)
                    
                    if is_valid_match:
                        # If it survived the filter, save both the P2 word and P1 fragment
                        p1_fragment = "".join(p1_derived_chars)
                        candidates.append((word, p1_fragment))
                        
    except FileNotFoundError:
        print(f"Error: Could not find the file '{csv_file_path}'")
        return

    # Print the mathematically possible pairs
    print(f"Found {len(candidates)} mathematically possible words for P2:\n")
    print(f"{'P2 Candidate Word':<25} | {'Resulting P1 Fragment':<25}")
    print("-" * 55)
    
    for p2_word, p1_frag in candidates:
        # We append 'hoboken ' to the P1 fragment to make it easier to read
        ret.append(p2_word)


# --- How to use this ---
# Replace 'dictionary.csv' with the actual path to your CSV file.
# If your CSV has headers, you might want to add `next(reader)` before the loop.
find_matching_words('./FrequentEnglishWordList.csv')

for i in range(len(ret)):
    print(ret[i])