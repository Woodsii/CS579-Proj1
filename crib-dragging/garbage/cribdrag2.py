import sys

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

def interactive_crib_drag(xor_data):
    length = len(xor_data)
    # Initialize two empty message buffers
    msg1 = ['_'] * length
    msg2 = ['_'] * length

    print(f"\n--- Interactive Crib Dragger ({length} bytes) ---")
    print("Commands:")
    print("  guess <pos> <word>  -> Guess a word at a position (e.g., 'guess 0 The')")
    print("  clear <pos> <len>   -> Clear a section")
    print("  show                -> Show current state")
    print("  exit                -> Quit")

    while True:
        print("\n" + "="*60)
        # Display the two messages aligned
        print("Msg 1: " + "".join(msg1))
        print("Msg 2: " + "".join(msg2))
        print("="*60)

        command = input("cmd> ").strip().split()
        if not command: continue

        action = command[0].lower()

        if action == 'exit':
            break

        elif action == 'show':
            continue

        elif action == 'guess':
            if len(command) < 3:
                print("Error: Usage 'guess <pos> <word>'")
                continue
                
            try:
                pos = int(command[1])
                guess_word = " ".join(command[2:]) # Handle words with spaces
                
                # Check bounds
                if pos + len(guess_word) > length:
                    print("Error: Guess is too long for the message.")
                    continue

                # Apply the logic: P2 = P1 ^ XOR
                # We assume the user is guessing for Msg 1. 
                # The math works nicely: The XOR difference reveals Msg 2.
                crib_bytes = guess_word.encode('utf-8')
                xor_segment = xor_data[pos : pos + len(crib_bytes)]
                
                revealed_bytes = bytes([a ^ b for a, b in zip(crib_bytes, xor_segment)])
                
                # Update our visual buffers
                for i, char in enumerate(guess_word):
                    msg1[pos + i] = char
                
                # Try to decode the revealed bytes to text
                try:
                    revealed_str = revealed_bytes.decode('ascii')
                    # Update Msg 2 with the revealed text
                    for i, char in enumerate(revealed_str):
                        # Simple filter to keep it readable
                        if 32 <= ord(char) <= 126:
                            msg2[pos + i] = char
                        else:
                            msg2[pos + i] = '?' # Mark non-printable chars
                except:
                    print("Warning: Revealed text contained non-ascii characters.")

            except ValueError:
                print("Error: Position must be a number.")

        elif action == 'clear':
            try:
                pos = int(command[1])
                length_clear = int(command[2])
                for i in range(length_clear):
                    if pos + i < length:
                        msg1[pos+i] = '_'
                        msg2[pos+i] = '_'
            except:
                print("Error: Usage 'clear <pos> <len>'")

# Run the tool
interactive_crib_drag(xored_plaintexts)