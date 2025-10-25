import csv
import os

input_path  = ".\\vokabeln\\Dictionary.csv"
learnedMin = 1

rows = []
with open(input_path, newline='', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    for row in reader:
        try:
            priority = int(row['Priority'])
            learned = int(row['Learned'])
        except ValueError:
            continue  # пропустить строки с плохими данными

        if learned >= learnedMin and row.get('Skip', '').strip() == '':
            rows.append(row)

rows.sort(key=lambda r: int(r['Priority']))

output_path = "./vokabeln/"
output_name = "Basic"
rows_per_file = 50  # количество строк в одном файле

# Убедимся, что путь существует
os.makedirs(output_path, exist_ok=True)

# Разбиваем на чанки
for i in range(0, len(rows), rows_per_file):
    chunk = rows[i:i+rows_per_file]
    file_index = i // rows_per_file + 1
    filename = f"{output_name}_{file_index:02}.csv"
    filepath = os.path.join(output_path, filename)

    with open(filepath, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['Question', 'Answer'])
        for row in chunk:
            writer.writerow([row['De'], row['Ru']])
