import os
import csv

input = ".\\cards\\themes\\я wo, da.csv"
wheres = [".\\cards\\exclude", ".\\cards\\lex", ".\\cards\\themes"]

def pr(txt):
    print(f"\r{(txt):<70}", end='', flush=True)

print()
print()

with open(input, encoding='utf-8') as f:
    reader = csv.DictReader(f)
    for i, row in enumerate(reader):
        # pr(f"{i}, {row["Question"]}, {row["Answer"]}")
        target_word = row["Question"].strip().lower()
        if target_word[0] == "~":
            continue

        for where in wheres:
            for filename in os.listdir(where):
                if not filename.endswith(".csv"):
                    continue
                filepath = os.path.join(where, filename)
                if filepath == input:
                    continue
                try:
                    with open(filepath, newline='', encoding='utf-8') as csvfile:
                        reader1 = csv.DictReader(csvfile)
                        for row1 in reader1:
                            if row1.get("Question").strip().lower() == target_word:
                                print(f"found: {target_word} in {filename}")
                except Exception as e:
                    print(f"error {filename}: {e}")
