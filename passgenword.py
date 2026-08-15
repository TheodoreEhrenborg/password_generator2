#!/usr/bin/env python3

"""Prints an xkcd-style passphrase of random words from a wordlist.
The default 6 words from the medium list (1650 words, 10.7 bits/word)
have 64.1 bits of entropy. The large list (7776 words, 12.9 bits/word)
needs 5 words for 64.6 bits; the short list (1296 words, 10.3 bits/word)
needs 7 for 72.4 bits."""
import argparse
import math
import secrets
import sys

parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument(
    "-n",
    "--words",
    type=int,
    default=6,
    help="number of words in the passphrase (default: 6)",
)
group = parser.add_mutually_exclusive_group()
group.add_argument(
    "--short",
    action="store_true",
    help="use the short wordlist (1296 words) instead of the medium one (1650)",
)
group.add_argument(
    "--large",
    action="store_true",
    help="use the large wordlist (7776 words); 5 words give 64.6 bits",
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
elif args.large:
    path, expected = "data/eff_large_wordlist.txt", 7776
else:
    path, expected = "data/medium_wordlist.txt", 1650

words = []
with open(path) as f:
    for line in f:
        # EFF lists have a dice-number column; the medium list (a modified
        # EFF list with uncommon words swapped for common ones) is words only
        word = line.split()[-1]
        words.append(word)

# Hard checks, not asserts: these must survive python -O
if len(words) != expected:
    sys.exit(f"{path}: expected {expected} words, found {len(words)}")
if len(set(words)) != expected:
    sys.exit(f"{path}: wordlist contains duplicates")
# Without this, a tampered list could contain Unicode homoglyph variants of
# the same word: unique as bytes, but identical when the user reads and
# retypes the passphrase, silently reducing effective entropy.
if not all(word.isascii() for word in words):
    sys.exit(f"{path}: wordlist contains non-ASCII characters")

entropy = args.words * math.log2(len(words))
if entropy < 64:
    print(
        f"Warning: {args.words} words from a {len(words)}-word list "
        f"give only {entropy:.1f} bits of entropy (< 64)",
        file=sys.stderr,
    )

print(args.separator.join(secrets.choice(words) for _ in range(args.words)))
