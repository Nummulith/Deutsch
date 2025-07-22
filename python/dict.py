import csv
import os

print("/n")

config_path = ".\\vokabeln\\Config.csv"
dictionary_file = ".\\vokabeln\\Dictionary.csv"

# Сначала — загрузим уже имеющиеся данные из Dictionary.csv (если он существует)
entries = {}
if os.path.exists(dictionary_file):
    with open(dictionary_file, mode='r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        # next(reader, None)  # пропустить заголовок
        for row in reader:
            entries[row["De"]] = row

with open(config_path, newline='', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    for row in reader:
        Path     = row["Path"]
        PriorMin = int(row["PriorMin"])
        PriorMax = int(row["PriorMax"])
        Learned  = int(row["Learned"])
        Skip     = row["Skip"]
        DeCol    = row["De"] if row["De"] else "De"
        print(f"{Path} : {PriorMin} < {PriorMax}, {Learned}, {Skip}")

        # Файлы
        filenames = []
        if Path.endswith(".csv"):
            filenames.append(Path)
        else:
            for filename in os.listdir(Path):
                if filename.endswith(".csv"):
                    filenames.append(os.path.join(Path, filename))

        # Обходим каждый файл
        header = "De,Ru,Priority,Learned,Skip".split(",")
        for filename in filenames:
            with open(filename, mode='r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                for newRow in reader:
                    De = newRow[DeCol]
                    dctRaw = entries.get(De, {})

                    setRaw = {}
                    for key in header:
                        val = ""

                        if key in dctRaw and dctRaw[key]:
                            val = dctRaw[key]

                        newKey = key
                        if newKey == "De":
                            newKey = DeCol
                        if newKey in newRow and newRow[newKey]:
                            val = newRow[newKey]

                        setRaw[key] = val

                    if not setRaw["Priority"]:
                        setRaw["Priority"] = PriorMax
                    if int(setRaw["Priority"]) < PriorMin:
                        setRaw["Priority"] = PriorMin
                    if int(setRaw["Priority"]) > PriorMax:
                        setRaw["Priority"] = PriorMax
                    if not setRaw["Learned"]:
                        setRaw["Learned"] = Learned
                    if setRaw["Learned"] == "-":
                        setRaw["Learned"] = 0
                    if not setRaw["Skip"]:
                        setRaw["Skip"] = Skip

                    entries[De] = setRaw

# Сохраняем результат в Dictionary.csv
entries = dict(sorted(entries.items()))
with open(dictionary_file, mode='w', encoding='utf-8', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(header)
    for key, row in entries.items():
        # resRaw = {key: row.get(key, "") for key in header}
        writer.writerow(row.values())
