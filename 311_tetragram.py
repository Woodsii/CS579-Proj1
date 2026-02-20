import math
import random
from collections import Counter, defaultdict
from pathlib import Path
import re

ALPHABET = list(" etaoinshrdlucmfwypvbgkjqxz.,'")  # includes space + punctuation

def load_cipher(path):
    s = Path(path).read_text(encoding="utf-8", errors="ignore")
    digits = "".join(ch for ch in s if ch.isdigit())
    if len(digits) % 3 != 0:
        raise ValueError("Ciphertext length not divisible by 3.")
    return [digits[i:i+3] for i in range(0, len(digits), 3)]

def load_quadgrams(path):
    # expected format: "TION 12345" per line
    quad = {}
    total = 0
    for line in Path(path).read_text(encoding="utf-8", errors="ignore").splitlines():
        line = line.strip()
        if not line:
            continue
        g, n = line.split()
        n = int(n)
        quad[g.lower()] = n
        total += n
    floor = math.log10(0.01 / total)
    logp = {g: math.log10(n / total) for g, n in quad.items()}
    return logp, floor

def score_english(text, logp, floor):
    t = re.sub(r"[^a-z ]", "", text.lower())
    t = t.replace(" ", "")
    s = 0.0
    for i in range(len(t) - 3):
        s += logp.get(t[i:i+4], floor)
    return s

def decode(tokens, mapping):
    return "".join(mapping[t] for t in tokens)

def random_init_mapping(codes):
    # bias: frequent codes more likely to be space/e/t/a/o/n
    mapping = {}
    for c in codes:
        mapping[c] = random.choice(ALPHABET)

    return mapping

def crack(tokens, logp, floor, steps=200000, T0=5.0, cooling=0.99995, sample_len=12000):
    sample = tokens[:min(sample_len, len(tokens))]
    codes = list(sorted(set(sample)))

    mapping = random_init_mapping(codes)

    # Frequency bias: push top codes toward common letters + space
    freq = Counter(sample)
    top_codes = [c for c, _ in freq.most_common(40)]
    common = list("     eeeeetttaaaooonnniisshhr")  # includes many spaces
    for c in top_codes:
        mapping[c] = random.choice(common)

    cur = decode(sample, mapping)
    cur_score = score_english(cur, logp, floor)
    best_score = cur_score
    best_map = mapping.copy()
    best_text = cur

    T = T0
    for step in range(steps):
        c = random.choice(codes)
        old = mapping[c]
        new = random.choice(ALPHABET)
        if new == old:
            T *= cooling
            continue

        mapping[c] = new
        cand = decode(sample, mapping)
        cand_score = score_english(cand, logp, floor)

        d = cand_score - cur_score
        if d >= 0 or random.random() < math.pow(10, d / max(T, 1e-9)):
            cur, cur_score = cand, cand_score
            if cand_score > best_score:
                best_score = cand_score
                best_map = mapping.copy()
                best_text = cand
        else:
            mapping[c] = old

        T *= cooling

    return best_map, best_text, best_score

if __name__ == "__main__":
    # change these:
    CIPHER_PATH = Path(r"C:\Users\Michael Buzzetta\Documents\CS579\CS579-Proj1\ctxts\13.txt")
    QUADGRAM_PATH = "english_quadgrams.txt"

    tokens = load_cipher(CIPHER_PATH)
    logp, floor = load_quadgrams(QUADGRAM_PATH)

    best_map, preview, sc = crack(tokens, logp, floor)

    # apply best map to full ciphertext (unknown codes show as [?])
    codes_full = set(tokens)
    mapping_full = {c: best_map.get(c, "?") for c in codes_full}
    plaintext = decode(tokens, mapping_full)

    print("=== PREVIEW (sample) ===")
    print(preview[:1000])
    print("\n=== FULL DECODE ===")
    print(plaintext)
