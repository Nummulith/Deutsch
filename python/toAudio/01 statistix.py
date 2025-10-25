import os
import csv
import re
from collections import Counter

# path  = '.\\out\\00 detect.txt'
# path  = '.\\course'
path = '.\\out\\01 statistix.csv'
output = '.\\out\\01 statistix1.csv'
enc = 'utf-8' # 'windows-1252'

with open(output, 'w', encoding='utf-8', newline='') as csvfile:
    writer = csv.writer(csvfile)

    filenames = []
    if path.endswith(".csv") or path.endswith(".txt"):
        filenames.append(path)
    else:
        for filename in os.listdir(path):
            if filename.endswith(".csv"):
                filenames.append(os.path.join(path, filename))

    for input in filenames:
        with open(input, 'r', encoding=enc) as f:
            text = f.read().lower()

#       r'\b[а-яa-zäöüßёÄÖÜẞ]+\b'
        words = re.findall(r'\b[a-zäöüßёÄÖÜẞ]+\b', text, re.IGNORECASE | re.UNICODE)
        word_counts = Counter(words)

        writer.writerow(['De', 'Num'])
        for word, count in word_counts.most_common():
            writer.writerow([word, count])
