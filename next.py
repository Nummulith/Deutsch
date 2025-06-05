import os
import csv

wheres = [".\\cards\\themes", ".\\cards\\lex"]
output = ".\\cards\\current\\Лексика.csv"
howMany = 100

def pr(txt):
    print(f"\r{(txt):<70}", end='', flush=True)

print()
print()

with open(output, 'w', encoding='utf-8', newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(["Question", "Answer"])
    writer.writerow(["~reverse", "True"])

    count = 0

    for where in wheres:
        for filename in os.listdir(where):
            if not filename.endswith(".csv"):
                continue
            filepath = os.path.join(where, filename)
            print(filepath)

            try:
                with open(filepath, newline='', encoding='utf-8') as csvfile:
                    reader1 = csv.DictReader(csvfile)
                    for row1 in reader1:
                        word = row1.get("Question")
                        ans  = row1.get("Answer")
                        if word[0] == "~":
                            continue
                        if len(row1) > 2:
                            continue

                        writer.writerow([word, ans])

                        count += 1
                        if count >= howMany:
                            break
            except Exception as e:
                print(f"error {filename}: {e}")

            if count >= howMany:
                break

        if count >= howMany:
            break
