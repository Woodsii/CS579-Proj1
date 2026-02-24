def load_blocks(filename):
    with open(filename, 'r') as f:
        data = f.read().strip()
        return [data[i:i+3] for i in range(0, len(data), 3)]

# The professor's hint
# Tossups: 672 -> a/i
# 213 -> t 
# 317 -> n
# 144 -> a/i
# 117 -> a/o

prof_map = {
    '158': ',', '770': '.', '659': '-', '799': '"', '648': "'",
    '662': ';', '460': '!', '296': '?', '477': '_', '885': '(',
    '275': ')', '331': ':', '955': '\n', '506': '\n', '309': '\n',
    
    "103": " ", "777": " ", "822": " ", "765": " ", "848": ' ',
    '686': ' ', '299': ' ',

    '394': '4', '186': '7',

    '590': 'a',
    '672': 'i',

    "523": "a",
    "225": "o",
    "756": "f",

    "380": 't',
    '796': 'h',
    '496': 'e',
    '178': 'n',
    
    "312": "e",
    "512": "n",
    '948': 'w',
    '101': 'r',
    '680': 'd',
    '708': 'o'
}


# files = ['03.txt', '11.txt', '19.txt', '20.txt']
files = ['19.txt']
for f in files: 

    blocks = load_blocks('./ctxts/' + f)

    decoded_text = ""
    for block in blocks: # Look at the first 150 blocks
        if block in prof_map:
            decoded_text += prof_map[block]
        else:
            decoded_text += ' '

    print(decoded_text)