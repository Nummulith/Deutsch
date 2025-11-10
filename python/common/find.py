import csv
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../')))
from common import wordsFrom

whats  = wordsFrom(["./source/lex.files", "./source/exclude/"])
wheres = wordsFrom("./source/levels/A2.csv")

def pr(txt):
    print(f"\r{(txt):<70}", end='', flush=True)

print()
print()

for what in whats:
    if what in wheres and whats[what] != wheres[what]:
        print(f"found: {what}: {whats[what]} / {wheres[what]}")
