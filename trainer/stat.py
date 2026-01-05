import matplotlib.pyplot as plt
from datetime import date, datetime, timedelta

import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../python/'))) # Добавляем в sys.path путь к папке python
from common_db import get_all, del_value

from settings import *

stats = get_all(DBs)
dates = [x['date' ] for x in stats.values()]
tasks = [x['tasks'] for x in stats.values()]
rem   = [x['remembered'] / timedelta(seconds = REMEMBERSEC) for x in stats.values()]
plt.plot(dates, rem, marker="o")
plt.title("Learning process")
plt.xlabel("Date")
plt.ylabel("Remembered")

# words = get_all(DB)
# index = [i for i, x in enumerate(words)]
# last  = [x['last'      ] for x in words.values()]
# rem   = [x['remembered'] / timedelta(seconds = REMEMBERSEC) for x in words.values()]
# rem   = sorted(rem, reverse=True)
# plt.plot(index, rem, marker="o")
# plt.title("Words remembered")
# plt.xlabel("Words")
# plt.ylabel("Remembered")

plt.show()
