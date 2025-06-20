#!/usr/bin/env python3
import json

hints = json.load(open("data/combined.json"))

password = input("Enter password (your typing will be visible)")

i = 0
while snippet := password[i : i + 3]:
    i += 3
    for hint in hints:
        if hint["short_text"] == snippet:
            print(hint)
