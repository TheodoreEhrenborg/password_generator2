#!/usr/bin/env python3

"""Builds data/eff_medium_wordlist.txt: the 1296 short-list words plus the
shortest large-list words not already present, up to 1650 words total.
6 words from 1650 give 64.1 bits of entropy. Hyphenated words are
excluded so every word stays distinct when read and retyped."""


def load(path):
    words = []
    with open(path) as f:
        for line in f:
            dice, word = line.split()
            words.append(word)
    return words

short = load("data/eff_short_wordlist_1.txt")
large = load("data/eff_large_wordlist.txt")
assert len(set(short)) == len(short) == 1296

combined = [w for w in short if "-" not in w]
extras = sorted(set(large) - set(short), key=lambda w: (len(w), w))
for word in extras:
    if len(combined) == 1650:
        break
    if "-" not in word:
        combined.append(word)

assert len(combined) == 1650
assert len(set(combined)) == 1650
assert all(word.isascii() and word.isalpha() and word.islower() for word in combined)

with open("data/eff_medium_wordlist.txt", "w") as f:
    for word in sorted(combined):
        f.write(word + "\n")
