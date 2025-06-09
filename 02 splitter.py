import csv
from collections import defaultdict

# https://github.com/repodiac/german_compound_splitter
from german_compound_splitter import comp_split

print("-")

dictionary = '.\\doc\\german.dic'
ahocs = comp_split.read_dictionary_from_file(dictionary)

input  = '.\\out\\statistix.csv'
output = ".\\out\\splitter.csv"

result_dict = defaultdict(int)

with open(input, encoding='utf-8') as f:
    reader = csv.DictReader(f)

    for i, row in enumerate(reader):
        compound = row["Wort"].strip()
        if not compound:
            continue

        try:
            num = int(row['Num'])
        except ValueError:
            continue  # Пропускаем строки с некорректным числом

        try:
            dissection = comp_split.dissect(compound, ahocs, make_singular=True)
            postMerge  = comp_split.merge_fractions(dissection)
        except Exception as e:
            postMerge = [compound]

        for word in postMerge:
            result_dict[word] += num

# Запись результата в CSV
with open(output, "w", encoding="utf-8", newline='') as f:
    writer = csv.writer(f)
    writer.writerow(["Wort", "Num"])
    for word, total in sorted(result_dict.items(), key=lambda x: -x[1]):
        writer.writerow([word, total])
