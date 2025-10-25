from bs4 import BeautifulSoup
import csv

input_file = '.\\htmlwords\\B1.html'
output_file = 'output.csv'

with open(input_file, 'r', encoding='utf-8') as f:
    soup = BeautifulSoup(f, 'html.parser')

rows = []

for td in soup.find_all('td'):
    parts = list(td.stripped_strings)
    if len(parts) >= 2:
        german_word = parts[0].strip()
        translation = parts[1].strip().strip('()')
        rows.append((german_word, translation))

# Сохраняем в CSV
with open(output_file, 'w', newline='', encoding='utf-8') as f:
    writer = csv.writer(f)
    writer.writerow(['German', 'Russian'])
    writer.writerows(rows)

print(f'Сохранено {len(rows)} слов в {output_file}')
