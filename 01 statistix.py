import csv
import re
from collections import Counter

input  = '.\\out\\detect.txt'
output = '.\\out\\statistix.csv'
enc = 'utf-8' # 'windows-1252'

with open(input, 'r', encoding=enc) as f:
    text = f.read().lower()

words = re.findall(r'\b[а-яa-zäöüßёÄÖÜẞ]+\b', text, re.IGNORECASE | re.UNICODE)
word_counts = Counter(words)

with open(output, 'w', encoding='utf-8', newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(['Wort', 'Num'])
    for word, count in word_counts.most_common():
        writer.writerow([word, count])
