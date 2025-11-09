import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../python/'))) # Добавляем в sys.path путь к папке python
from common import wordsFromCfg
from common_db import set_value, get_value

DB = "trainer/data.db"
config_path = ".\\source\\lex.files"

print("\n.")

# Пример использования
set_value(DB, "username", {"clex": "alex", "age": 30})
print(get_value(DB, "username"))   # -> alex
print(get_value(DB, "age", 42))    # -> 42 (если ключа нет)

words = wordsFromCfg(config_path, count = 100)

print(words)
