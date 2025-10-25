import os
import csv

def filesFromCfg(config_path):
    with open(config_path, newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        filenames = []
        for row in reader:
            Path     = row["Path"]
            if Path.endswith(".csv"):
                filenames.append(Path)
            else:
                for filename in os.listdir(Path):
                    if filename.endswith(".csv"):
                        filenames.append(os.path.join(Path, filename))
    return filenames

def wordsFromFile(dictionary_file):
    entries = {}
    if os.path.exists(dictionary_file):
        with open(dictionary_file, mode='r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            DeKey = "De" if "De" in reader.fieldnames else "Question"
            RuKey = "Ru" if "Ru" in reader.fieldnames else "Answer"
            for row in reader:
                De = row[DeKey]
                Ru = row[RuKey]
                if De[0] == "~":
                    continue
                entries[De] = Ru
    return entries

def wordsFromCfg(config_path, ex = None, count = None):
    filenames = filesFromCfg(config_path)

    words = {}
    co = 0
    for filename in filenames:
        # print(filename)

        for De, Ru in wordsFromFile(filename).items():
            if ex and De in ex:
                continue

            words[De] = Ru

            co += 1
            if count and co >= count:
                break

        if count and co >= count:
            break

    return words

def wordsToFile(words, filename):
    header = "De,Ru".split(",")
    entries = dict(sorted(words.items()))
    with open(filename, mode='w', encoding='utf-8', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(header)
        for key, row in entries.items():
            # resRaw = {key: row.get(key, "") for key in header}
            val = [key, row] if isinstance(row, str) else row.values()
            writer.writerow(val)
