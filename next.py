import os
import csv

# wheres = [".\\cards\\themes", ".\\cards\\lex"]
wheres = [".\\cards\\test"]
output_dir = ".\\cards\\current"
howMany = 50

def pr(txt):
    print(f"\r{(txt):<70}", end='', flush=True)

print("-")

file_index = 1
count_in_file = 0
total_count = 0

def create_new_writer(file_index):
    prefix = "Тест"
    filename = os.path.join(output_dir, f"{prefix} {file_index:02}.csv")
    f = open(filename, 'w', encoding='utf-8', newline='')
    writer = csv.writer(f)
    writer.writerow(["Question", "Answer"])
    writer.writerow(["~reverse", "True"])
    return f, writer

output_file, writer = create_new_writer(file_index)

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

                    if not word or not ans:
                        continue
                    if word[0] == "~":
                        continue
                    if len(row1) > 2:
                        continue

                    writer.writerow([word, ans])
                    count_in_file += 1
                    total_count += 1

                    if count_in_file >= howMany:
                        output_file.close()
                        file_index += 1
                        count_in_file = 0
                        output_file, writer = create_new_writer(file_index)

        except Exception as e:
            print(f"error {filename}: {e}")

output_file.close()
print(f"\n\nTotal entries written: {total_count}")
