import csv
import re
from collections import Counter

input  = '.\\out\\detect.txt'
# input = "sub_morph.csv"
output = '.\\out\\statistix.csv'
# output = "sub_morph_stat.csv"

# enc = 'windows-1252'
enc = 'utf-8'

with open(input, 'r', encoding=enc) as f:
    text = f.read().lower()

# Извлекаем слова: учитываются только буквы, в том числе кириллица
words = re.findall(r'\b[а-яa-zäöüßёÄÖÜẞ]+\b', text, re.IGNORECASE | re.UNICODE)

# Подсчёт количества слов
word_counts = Counter(words)

# Сохраняем статистику в CSV
with open(output, 'w', encoding='utf-8', newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(['Wort', 'Num'])
    for word, count in word_counts.most_common():
        writer.writerow([word, count])
