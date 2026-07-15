import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../python/'))) # Добавляем в sys.path путь к папке python
from common import wordsFrom, randomDict, filesFromFiles, wordsFromFile
from common_db import get_all, set_value, get_value

from datetime import date, datetime, timedelta

from settings import *

all = get_all(DB)
# print(all)

filename = "progress.txt"

def time_to_string(dt: datetime) -> str:
    """
    Преобразует datetime в строку формата "ГГГГ|М|Д|Ч|М|С"
    Пример: datetime.datetime(2026, 1, 25, 20, 32, 58, 493272) -> "2026|1|25|20|32|58"
    """
    return f"{dt.year}|{dt.month}|{dt.day}|{dt.hour}|{dt.minute}|{dt.second}"

def delta_to_string(td: timedelta) -> str:
    """
    Преобразует timedelta в строку с количеством секунд (с плавающей точкой)
    Пример: datetime.timedelta(days=17, seconds=40408, microseconds=538986) -> "1509208.538986"
    """
    total_seconds = td.total_seconds()
    return f"{total_seconds:.6f}"  # 6 знаков после запятой для микросекунд



with open(filename, "w", encoding="utf-8") as file:
    pass  # просто открыли и закрыли — файл очищен

with open(filename, "a", encoding="utf-8") as file:
    for word, dt in all.items():
        last = dt["last"]
        reme = dt["remembered"]
        file.write(""\
            + word + ";"\
            + time_to_string (last) + ";"\
            + delta_to_string(reme) + "\n")
