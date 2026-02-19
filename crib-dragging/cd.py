
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

        if pos and not pos == i:
            continue
        chunk = xor_data[i : i + len(crib)]

        result = bytes([a ^ b for a, b in zip(chunk, crib)])
        
        try:
            decoded = result.decode('ascii')
            if all(32 <= ord(c) <= 126 for c in decoded):
                print(f"--- Dragging crib: '{crib_str[:10]}...' ---")
                print(f"Pos {i}: {decoded}")
        except:
            pass


# --------------------------------------------------------------

def getKey(M, CTXT):
    M = M.encode('utf-8')

    return bytes([a ^ b for a, b in zip(M, CTXT)])

def removeFogOfWar():
    M = 'the enigma machine, a german rotor cipher, mixed letters through shifting wiring and a plugboard, yielding vast keyspaces. daily keys and message procedures guarded secrecy, yet operator habits leaked patterns. allied analysts combined math, crib-finding, and polish insights, building electromechanical bombes to test permutations. bletchley park turned signals into intelligence, shortening the war and proving computation plus rigor can pierce layered secrecy without brute force.'

    k = getKey(M, ctxts[2])
    
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

# hoboken began as lenape homeland. dutch settlers arrived in the seventeenth century. later, the stevens family shaped its growth with industry and education,
# founding stevens institute of technology. the city became a hub for shipping and manufacturing during the nineteenth century. immigrants brought culture and
# resilience. music and arts flourished; frank sinatra rose from its lively streets. today, hoboken stands as a vibrant community along hudson river with 
# historic charm, modern spirit and [missing]

# in the attention economy, time is bartered for flickers of novelty. platforms design infinite scroll, alerts, and streaks to harvest focus, converting 
# glances into revenue. algorithms model desire, amplify outrage, and reward impulsive taps, optimizing for engagement above meaning. creators chase metrics
# while audiences drift, auctioning their concentration to the highest bidder. attention becomes the scarce resource, shaping behavior and taste in a market 
# where distraction is king. 

# the enigma machine, a german rotor cipher, mixed letters through shifting wiring and a plugboard, yielding vast keyspaces. daily keys and message procedures 
# guarded secrecy, yet operator habits leaked patterns. allied analysts combined math, crib-finding, and polish insights, building electromechanical bombes to 
# test permutations. bletchley park turned signals into intelligence, shortening the war and proving computation plus rigor can pierce layered secrecy without 
# brute force.

# chicago rose at a crossroads of water and rail, rebuilt after the 1871 fire with steel frames and daring architects who birthed skyscrapers. stockyards, 
# canals, and grain shaped commerce, while neighborhoods forged music, activism, and resilient culture. the lakefront sets wind against glass towers, trains 
# thread alleys, and grids map ambitious across prarie. the city endures booms and storms, reinventing itself with grit, invention, and a taste for big ideas 
# under a wide midwestern sky.

# --------------------------------------------------------------

'''Workspace'''

removeFogOfWar()

IND1 = 0
IND2 = 2
OFFSET = 314

xored_plaintexts = bytes([a ^ b for a, b in zip(ctxts[IND1], ctxts[IND2])])

# print(f"length of XORed CTXTs: {len(xored_plaintexts)}")

crib = " resilience. music and arts flourished; frank sinatra rose from its lively streets. today, hoboken stands as a vibrant community along hudson river with historic charm, modern spirit"

# drag_crib(crib, xored_plaintexts, OFFSET)
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
