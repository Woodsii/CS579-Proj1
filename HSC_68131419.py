from pathlib import Path

CIPHERTEXT_PATH = Path(r"C:\Users\Michael Buzzetta\Documents\CS579\CS579-Proj1\ctxts\13.txt")

MAP = {
    "391": " ",
    "287": ".",
    "452": ",",
    "174": ",",

    "606": "e",
    "657": "t",
    "615": "a",
    "622": "o",
    "599": "s",
    "525": "n",
    "737": "d",
    "441": "i",
    "303": "r",
    "468": "h",
    "954": "l",
    "739": "b",
    "211": "c",
    "896": "g",
    "961": "w",
    "949": "u",
    "406": "p",
    "867": "y",
    "184": "f",
    "464": "m",
    "120": "v",
    "686": "z",
    "218": "k",
    "053": "q",
}

def chunk3(s: str):
    s = "".join(ch for ch in s if ch.isdigit())
    if len(s) % 3 != 0:
        raise ValueError(f"Ciphertext length {len(s)} is not divisible by 3.")
    return [s[i:i+3] for i in range(0, len(s), 3)]

def decode(cipher_digits: str) -> str:
    chunks = chunk3(cipher_digits)
    out = []
    unknown = set()

    for c in chunks:
        if c in MAP:
            out.append(MAP[c])
        else:
            unknown.add(c)
            out.append(f"[{c}]")

    if unknown:
        print("Unknown codes found:", ", ".join(sorted(unknown)))

    return "".join(out)

if __name__ == "__main__":
    print("We started by finding the demoninator. We attempted all numbers from 1-9, and found that 3 was the most likely value, so every character was tied to a distinct three digit sequence.")
    print("Once we determined that, we found that the sequence 391 was the most prevelant by far, and assumed it must be a [space] character, so we replaced all 391 with a ' '.")
    print("This allowed us to determine the length of words, and we found that the second word (Third sequence post 391 replacement) was a single character, so that narrowed down the possible letters to A and I.")
    print("From there, we determined several other characters, focusing primarily on short, easy to discern words and phrases.")
    ciphertext = CIPHERTEXT_PATH.read_text(encoding="utf-8", errors="ignore")
    plaintext = decode(ciphertext)
    print(plaintext)
