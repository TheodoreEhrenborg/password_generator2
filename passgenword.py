#!/usr/bin/env python3

"""Prints an xkcd-style passphrase of random words from an EFF wordlist.
With the large list (7776 words, 12.9 bits/word), the default
5 words have 64.6 bits of entropy. The short list (1296 words,
10.3 bits/word) needs 7 words to exceed 64 bits."""
import argparse
import math
import secrets
import sys

parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument(
    "-n",
    "--words",
    type=int,
    default=5,
    help="number of words in the passphrase (default: 5)",
)
group = parser.add_mutually_exclusive_group()
group.add_argument(
    "--short",
    action="store_true",
    help="use the short wordlist (1296 words) instead of the large one (7776)",
)
group.add_argument(
    "--medium",
    action="store_true",
    help="use the medium wordlist (1650 words); 6 words give 64.1 bits",
)
parser.add_argument(
    "-s",
    "--separator",
    default=" ",
    help="separator between words (default: space)",
)
args = parser.parse_args()

if args.short:
    path, expected = "data/eff_short_wordlist_1.txt", 1296
elif args.medium:
    path, expected = "data/eff_medium_wordlist.txt", 1650
else:
    path, expected = "data/eff_large_wordlist.txt", 7776

words = []
with open(path) as f:
    for line in f:
        # EFF lists have a dice-number column; the medium list is words only
        word = line.split()[-1]
        words.append(word)

assert len(words) == expected
assert len(set(words)) == expected
# Without this, a tampered list could contain Unicode homoglyph variants of
# the same word: unique as bytes, but identical when the user reads and
# retypes the passphrase, silently reducing effective entropy.
assert all(word.isascii() for word in words)

entropy = args.words * math.log2(len(words))
if entropy < 64:
    print(
        f"Warning: {args.words} words from a {len(words)}-word list "
        f"give only {entropy:.1f} bits of entropy (< 64)",
        file=sys.stderr,
    )

print(args.separator.join(secrets.choice(words) for _ in range(args.words)))
