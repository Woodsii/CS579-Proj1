from pathlib import Path
from collections import Counter

CIPHERTEXT_PATH = Path(r"C:\Users\Michael Buzzetta\Documents\CS579\CS579-Proj1\ctxts\03.txt")


MAP = {
    "765": " ",
    "451": " ",
    "256": " ",
    "165": " ",
    "586": " ",
    "613": " ",
    "848": " ",
    "395": " ", 
    "436": " ", 
    "825": " ", 
    "948": " ",
    "158": ",",
    "770": ".",
    "659": "-",
    "799": '"',
    "648": "'",
    "662": ";",
    "460": "!",
    "296": "?",
    "477": "_",
    "885": "(",
    "275": ")",
    "331": ":",
    "955": "\n",
    "506": "\n",
    "309": "\n",
    "394": "4",
    "186": "7",
    "443": "i",
    "457": "a",
    "101": "h",
    "117": "h",
    "903": "e",
    "590": "t",
    "376": "t",
    "312": "h",
    "580": "s",
    "370": "o",
    "189": "t",
    "679": "s",
    "380": "u",
    "672": "w",
    "760": "i",
    "357": "s",
    "822": "r",
    "273": "n",
    "496": "l",
    "103": "r",
    "111": "l",
    "127": "f",
    "130": "d",
    "144": "c",
    "175": "p",
    "178": "g",
    "188": " ",
    "199": "m",
    "201": " ",
    "213": "s",
    "225": "n",
    "231": " ",
    "253": "y",
    "260": "v",
    "262": " ",
    "279": "k",
    "299": "i",
    "303": "h",
    "324": "w",
    "342": "v",
    "368": "e",
    "371": "t",
    "372": "o",
    "387": "a",
    "400": "n",
    "430": "e",
    "434": "u",
    "495": ",",
    "975": "o",
    "939": "h",
    "621": "u",
    "638": "c",
    "756": "e",
    "783": "w",
    "564": "a",
    "704": "b",
    "685": "i",
    "722": "n",
    "548": "h",
    "593": "h",
    "851": "u",
    "805": "c",
    "448": "o",
    "565": "e",
    "692": "t",
    "695": "t",
    "744": "t",
    "530": "g",
    "833": "l",
    "796": "r",
    "317": "y",
    "562": "n",
    "881": "o",
    "456": "f",
    "243": "t",
    "752": "h",
    "523": "r",
    "686": "s",
    "737": "l",
    "109": "e",
    "777": "s",
    "769": "a",
    "914": "d",
    "857": "m",
    "751": "i",
    "680": "o",
    "573": "h",
    "381": "c",
    "386": "b",
    "847": "r",
    "708": "p",
    "717": "w",
    "775": "e",
    "512": "l",
    "734": "i",
    "797": "j",
    "306": "t",
    "431": "q",
    "154": "x",   
}

def chunk3(s: str):
    s = "".join(ch for ch in s if ch.isdigit())
    if len(s) % 3 != 0:
        raise ValueError(f"Ciphertext length {len(s)} is not divisible by 3.")
    return [s[i:i+3] for i in range(0, len(s), 3)]

def decode(cipher_digits: str, top_n: int = 25):
    chunks = chunk3(cipher_digits)
    out = []
    unknown_counts = Counter()

    for c in chunks:
        if c in MAP:
            out.append(MAP[c])
        else:
            unknown_counts[c] += 1
            out.append(f"[{c}]")

    plaintext = "".join(out)

    words = plaintext.split()
    two_letter = Counter()
    three_letter = Counter()

    for w in words:
        if w.startswith("[") and w.endswith("]"):
            inner = w[1:-1]
            parts = inner.split("][")
            if len(parts) == 2:
                two_letter[w] += 1
            elif len(parts) == 3:
                three_letter[w] += 1

    print(f"Total 3-digit symbols: {len(chunks)}")
    print(f"Distinct unknown symbols: {len(unknown_counts)}")

    if unknown_counts:
        print("\nTop unknown symbols by frequency:")
        for code, cnt in unknown_counts.most_common(top_n):
            print(f"{code}: {cnt}")

    print("\nTop 2-letter words (as code-pairs):")
    for w, cnt in two_letter.most_common(15):
        print(f"{w}: {cnt}")

    print("\nTop 3-letter words (as code-triples):")
    for w, cnt in three_letter.most_common(15):
        print(f"{w}: {cnt}")

    return plaintext, unknown_counts, two_letter, three_letter

if __name__ == "__main__":
    ciphertext = CIPHERTEXT_PATH.read_text(encoding="utf-8", errors="ignore")
    plaintext, unknown_counts, two_letter, three_letter = decode(ciphertext, top_n=30)

    print("\n--- DECODED (PARTIAL) OUTPUT START ---\n")
    print(plaintext[:5000])
    print("\n--- DECODED (PARTIAL) OUTPUT END ---\n")

    out_path = CIPHERTEXT_PATH.with_name("03_partial_decoded.txt")
    out_path.write_text(plaintext, encoding="utf-8")
    print(f"Wrote full partial decode to: {out_path}")