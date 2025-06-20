#!/usr/bin/env python3

"""Prints out 14 random lowercase letters.
One letter has 4.7 bits of entropy, so 14 letters
have 65.8 bits"""
import secrets

letters = "abcdefghijklmnopqrstuvwxyz"
assert len(letters) == 26
assert len(set(letters)) == 26
password = ""
for i in range(14):
    password += secrets.choice(letters)
print(password)
