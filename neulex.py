import os
import csv

input  = ".\\subs\\wa_morph.csv"
# input  = ".\\03 Лексика.csv"
wheres = [".\\cards\\lex", ".\\cards\\themes", ".\\cards\\exclude"]
output = ".\\lex.csv"

def pr(txt):
    print(f"\r{(txt):<70}", end='', flush=True)

print()
print()

with open(input, encoding='utf-8') as f:
    reader = csv.DictReader(f)

    with open(output, 'w', encoding='utf-8', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["Question"])

        count = 0

        for i, row in enumerate(reader):
            # pr(f"{i}, {row["Question"]}, {row["Answer"]}")
            target_word = row["Wort"].strip()
            if target_word[0] == "~":
                continue
            if "Pos" in row and (row["Pos"] == "VERB" or row["Pos"] == "AUX" or row["Pos"] == "ADJ" or row["Pos"] == "PRON"):
                target_word = row["Lemma"]
                target_word = target_word.lower()
            elif "Pos" in row and row["Pos"] == "NOUN":
                target_word = row["Lemma"]
                target_word = target_word.capitalize()
                if row["Gender"] == "Masc":
                    target_word = "der " + target_word
                if row["Gender"] == "Neut":
                    target_word = "das " + target_word
                if row["Gender"] == "Fem":
                    target_word = "die " + target_word
            else:
                target_word = target_word.lower()

            found = False
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
                                if row1.get("Question").strip() == target_word:
                                    # print(f"found: {target_word} in {filename}")
                                    found = True
                    except Exception as e:
                        print(f"error {filename}: {e}")

            if found:
                continue

            writer.writerow([target_word])

            count += 1
            if count >= 100:
                break
