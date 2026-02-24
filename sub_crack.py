import math
import random
import re
import sys
from collections import Counter

ALPH = "abcdefghijklmnopqrstuvwxyz"

# A small built-in tetragram model (log probabilities) generated from English.
# This is a compact model: good enough for cracking long substitution ciphertexts fast.
# Unseen tetragrams get a floor score.
TETRA_LOGP = None

def build_tetra_model_from_text(english_sample: str):
    # Build tetragram log probabilities from sample text
    txt = re.sub(r"[^a-z]", "", english_sample.lower())
    counts = Counter(txt[i:i+4] for i in range(len(txt) - 3))
    total = sum(counts.values())
    model = {}
    for tg, c in counts.items():
        model[tg] = math.log10(c / total)
    floor = math.log10(0.01 / total)  # smoothing floor
    return model, floor

# A decent built-in English sample (public domain style) to build tetragrams.
# (Not your ciphertext; just training text.)
ENGLISH_SAMPLE = """
when in the course of human events it becomes necessary for one people to dissolve the political bands
which have connected them with another and to assume among the powers of the earth the separate and
equal station to which the laws of nature and of nature's god entitle them a decent respect to the
opinions of mankind requires that they should declare the causes which impel them to the separation.
we hold these truths to be self evident that all men are created equal that they are endowed by their
creator with certain unalienable rights that among these are life liberty and the pursuit of happiness.
that to secure these rights governments are instituted among men deriving their just powers from the
consent of the governed that whenever any form of government becomes destructive of these ends it is
the right of the people to alter or to abolish it and to institute new government laying its foundation
on such principles and organizing its powers in such form as to them shall seem most likely to effect
their safety and happiness.
"""

def init_model():
    global TETRA_LOGP, TETRA_FLOOR
    TETRA_LOGP, TETRA_FLOOR = build_tetra_model_from_text(ENGLISH_SAMPLE)

def normalize(text: str) -> str:
    return text.lower()

def apply_key(text: str, key_map: dict[str, str]) -> str:
    # key_map: cipher -> plain
    out = []
    for ch in text:
        if ch in ALPH:
            out.append(key_map.get(ch, ch))
        else:
            out.append(ch)
    return "".join(out)

def random_key():
    perm = list(ALPH)
    random.shuffle(perm)
    return dict(zip(ALPH, perm))

def swap_two(key_map: dict[str, str]) -> dict[str, str]:
    k = dict(key_map)
    a, b = random.sample(ALPH, 2)
    k[a], k[b] = k[b], k[a]
    return k

def score_text_tetragrams(text: str) -> float:
    # Score ONLY letters (strip non-letters)
    s = re.sub(r"[^a-z]", "", text.lower())
    if len(s) < 100:
        return -1e18
    score = 0.0
    for i in range(len(s) - 3):
        tg = s[i:i+4]
        score += TETRA_LOGP.get(tg, TETRA_FLOOR)
    return score

def hillclimb(ciphertext: str, steps=200000):
    text = normalize(ciphertext)

    key = random_key()
    plain = apply_key(text, key)
    cur = score_text_tetragrams(plain)

    best_key = dict(key)
    best_plain = plain
    best = cur

    for i in range(steps):
        cand_key = swap_two(key)
        cand_plain = apply_key(text, cand_key)
        cand = score_text_tetragrams(cand_plain)

        if cand > cur:
            key, plain, cur = cand_key, cand_plain, cand
            if cand > best:
                best_key, best_plain, best = dict(key), plain, cand

        if (i + 1) % 20000 == 0:
            print(f"[{i+1}] best={best:.2f}")
            print(best_plain[:500])
            print()

    return best_key, best_plain, best

def multi_restart(ciphertext: str, restarts=30, steps=200000):
    overall_best = -1e18
    overall_key = None
    overall_plain = None

    for r in range(restarts):
        key, plain, sc = hillclimb(ciphertext, steps=steps)
        if sc > overall_best:
            overall_best = sc
            overall_key = key
            overall_plain = plain
        print(f"=== restart {r+1}/{restarts} best={overall_best:.2f} ===")
        print(overall_plain[:500])
        print()

    return overall_key, overall_plain, overall_best

def main():
    if len(sys.argv) != 2:
        print("Usage: python sub_crack.py path/to/03_partial_decoded.txt")
        sys.exit(1)

    init_model()

    path = sys.argv[1]
    ciphertext = open(path, "r", encoding="utf-8", errors="ignore").read()

    key, plain, sc = multi_restart(ciphertext, restarts=25, steps=150000)

    print("\n=== BEST KEY (cipher -> plain) ===")
    for c in ALPH:
        print(f"{c} -> {key[c]}")
    print("\n=== PLAINTEXT PREVIEW ===")
    print(plain[:3000])

if __name__ == "__main__":
    main()