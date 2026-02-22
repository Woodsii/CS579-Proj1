from pathlib import Path
from collections import Counter

CIPHERTEXT_PATH = Path(r"C:\Users\Michael Buzzetta\Documents\CS579\CS579-Proj1\ctxts\03.txt")

SPACE_CODES = {
    "765", "451", "256", "165", "586",
    "613", "848", "395", "436", "825", "948"
}

MAP = {
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
    "443": "I",
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
    # "109": "?",
    # "154": "?",
    # "199": "?",
    # "243": "?",
    # "306": "?",
    # "317": "?",
    # "381": "?",
    # "386": "?",
    # "431": "?",
    # "448": "?",
    # "456": "?",
    # "496": "?",
    # "512": "?",
    # "523": "?",
    # "530": "?",
    # "548": "?",
    # "562": "?",
    # "564": "?",
    # "565": "?",
    # "573": "?",
    # "593": "?",
    # "621": "?",
    # "638": "?",
    # "672": "?",
    # "680": "?",
    # "685": "?",
    # "686": "?",
    # "692": "?",
    # "695": "?",
    # "704": "?",
    # "708": "?",
    # "717": "?",
    # "722": "?",
    # "734": "?",
    # "737": "?",
    # "744": "?",
    # "751": "?",
    # "752": "?",
    # "756": "?",
    # "760": "?",
    # "769": "?",
    # "775": "?",
    # "777": "?",
    # "783": "?",
    # "796": "?",
    # "797": "?",
    # "805": "?",
    # "822": "?",
    # "833": "?",
    # "847": "?",
    # "851": "?",
    # "857": "?",
    # "881": "?",
    # "914": "?",
    # "939": "?",
    # "975": "?",
}

for code in SPACE_CODES:
    MAP[code] = " "

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