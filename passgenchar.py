#!/usr/bin/env python3

"""Prints out random lowercase letters.
One letter has 4.7 bits of entropy, so the default
14 letters have 65.8 bits"""
import argparse
import math
import secrets
import sys

letters = "abcdefghijklmnopqrstuvwxyz"
assert len(letters) == 26
assert len(set(letters)) == 26
assert round(math.log2(26), 1) == 4.7
assert round(14 * math.log2(26), 1) == 65.8

parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument(
    "-n",
    "--length",
    type=int,
    default=14,
    help="number of letters in the password (default: 14)",
)
args = parser.parse_args()

entropy = args.length * math.log2(len(letters))
if entropy < 64:
    print(
        f"Warning: {args.length} letters give only {entropy:.1f} bits of entropy (< 64)",
        file=sys.stderr,
    )

password = ""
for i in range(args.length):
    password += secrets.choice(letters)
print(password)
