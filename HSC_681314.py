from pathlib import Path

CIPHERTEXT_PATH = Path(r"C:\Users\Michael Buzzetta\Documents\CS579\CS579-Proj1\ctxts\19.txt")

MAP = {
    "391": " ",
    "287": ".",
    "452": ",",
    "174": ",",
    "044": "x",
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
    ciphertext = CIPHERTEXT_PATH.read_text(encoding="utf-8", errors="ignore")
    plaintext = decode(ciphertext)
    print(plaintext)
