import os
import csv
import random

def filesFromFiles(files_path):
    filenames = []
    if isinstance(files_path, list):
        for filename in files_path:
            filenames += filesFromFiles(filename)
    elif files_path.endswith(".files"):
        with open(files_path, newline='', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                filename = row["Path"]
                filenames += filesFromFiles(filename)
    elif files_path.endswith(".csv"):
        filenames += [files_path]
    else: # folder
        for filename in os.listdir(files_path):
            filenames += filesFromFiles(os.path.join(files_path, filename))
    return filenames

def wordsFromFile(filename):
    entries = {}
    if os.path.exists(filename):
        with open(filename, mode='r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            DeKey = "De" if "De" in reader.fieldnames else "Question"
            RuKey = "Ru" if "Ru" in reader.fieldnames else "Answer"
            forward = True
            reverse = False
            for row in reader:
                De = row[DeKey]
                if not De: De = ""
                De = De.strip()

                Ru = row[RuKey]
                if not Ru: Ru = ""
                Ru = Ru.strip()

                if De[0] == "~":
                    if De == "~forward":
                        forward = Ru.lower() == "true"
                    elif De == "~reverse":
                        reverse = Ru.lower() == "true"
                    continue

                if forward:
                    if De in entries and Ru != entries[De]:
                        print(f"Duplicate word <{De}> inside {filename} : {Ru} / {entries[De]}")
                    entries[De] = Ru

                if reverse:
                    if Ru in entries and De != entries[Ru]:
                        print(f"Duplicate word <{Ru}> inside {filename} : {De} / {entries[Ru]}")
                    entries[Ru] = De

    return entries

def wordsFrom(files_path, ex = None, count = None):
    filenames = filesFromFiles(files_path)

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

def randomDict(source):
    items = list(source.items())
    random.shuffle(items)
    return dict(items)
