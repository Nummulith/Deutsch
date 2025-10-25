import sys
import os
import csv

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))) # Добавляем в sys.path путь к папке python
from common import filesFromCfg, wordsFromFile, wordsToFile, wordsFromCfg

print("\n")

config_path = ".\\source\\lex.files"
except_path = ".\\vokabeln\\vokabeln.files"
output_file = ".\\vokabeln\\vokabeln_3.csv"

ex = wordsFromCfg(except_path)

words = wordsFromCfg(config_path, ex = ex, count = 100)

wordsToFile(words, output_file)
