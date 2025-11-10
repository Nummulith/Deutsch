import sys
import os
import csv

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))) # Добавляем в sys.path путь к папке python
from common import filesFromFiles, wordsFromFile, wordsToFile, wordsFrom

print("\n")

config_path = ".\\source\\lex.files"
except_path = ".\\vokabeln\\vokabeln.files"
output_file = ".\\vokabeln\\vokabeln_3.csv"

ex = wordsFrom(except_path)

words = wordsFrom(config_path, ex = ex, count = 100)

wordsToFile(words, output_file)
