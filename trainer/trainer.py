# from pyinstrument import Profiler

import math
from datetime import datetime, timedelta

from PyQt5 import QtWidgets, uic, QtGui
from PyQt5.QtCore import Qt, QRectF

import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../python/'))) # Добавляем в sys.path путь к папке python
from common import wordsFrom, randomDict, filesFromFiles, wordsFromFile
from common_db import get_all, set_value, get_value

THEME = "lex"
FILES = f"./source/{THEME}.files"
DB  = f"./trainer/{THEME}.db"

# THEME = "course"
# FILES = f"./course/{THEME}.files"
# DB  = f"./trainer/{THEME}.db"

MEMORYUP   = 2.1
MEMORYDOWN = 2.5
WINRATIO   = 0.8

def ChangeExt(path, new_ext):
    base, _ = os.path.splitext(path)
    return base + new_ext

def short_timedelta(delta: timedelta) -> str:
    total_seconds = int(delta.total_seconds())
    days = total_seconds // 86400
    if days > 0:
        return f"{days} дн"
    hours = total_seconds // 3600
    if hours > 0:
        return f"{hours} ч"
    minutes = total_seconds // 60
    if minutes > 0:
        return f"{minutes} мин"
    return f"{total_seconds} сек"

class DiagramWidget(QtWidgets.QWidget):
    def __init__(self, window_):
        super().__init__()
        self.window = window_
        # self.setMinimumSize(400, 200)
        self.setSizePolicy(
            QtWidgets.QSizePolicy.Expanding,  # по ширине тянется
            QtWidgets.QSizePolicy.Fixed       # по высоте фиксирована
        )
        self.setMinimumHeight(150)

    def paintEvent(self, event):
        wnd = self.window

        qp = QtGui.QPainter(self)
        qp.setRenderHint(QtGui.QPainter.Antialiasing)

        words = wnd.index
        n = len(words)
        if n == 0:
            return

        w, h = self.width(), self.height()

        # вычисляем число колонок так, чтобы квадраты целиком влезли по вертикали
        cols = int((w / h * n) ** 0.5) or 1
        rows = (n + cols - 1) // cols

        # вычисляем размер квадрата
        size = min(w / cols, h / rows)

        now = datetime.now()

        filesExp = 0

        # если есть "лишнее" пространство — не центрируем, просто обрезаем
        for i, q in enumerate(words):
            col = i % cols
            row = i // cols
            x = col * size
            y = row * size
            if y >= h:  # за границей формы — не рисуем
                break
            ratio  = wnd.ratios [q]
            expire = wnd.expires[q]
            qp.fillRect(QRectF(x, y, size, size), ratio2color(ratio, expire < now))

            if not expire < now:
                filesExp += 1

        qp.end()

        wnd.label_total.setText(f"rmb {wnd.ratioCur / wnd.ratioMax:.2f} = {wnd.ratioCur:.2f} / {int(wnd.ratioMax)}")
        wnd.paintLabel(wnd.label_total, wnd.ratioCur / wnd.ratioMax)

        wnd.label_files.setText(f"fls {wnd.filesCur / wnd.filesMax:.2f} = {int(wnd.filesCur)} / {int(wnd.filesMax)}")
        wnd.paintLabel(wnd.label_files, wnd.filesCur / wnd.filesMax)

        wnd.label_words.setText(f"lrn {filesExp / wnd.ratioMax:.2f} = {int(filesExp)} / {int(wnd.ratioMax)}")
        wnd.paintLabel(wnd.label_words, filesExp / wnd.ratioMax)

def timedelta2ratio(td: timedelta):
    total_seconds = td.total_seconds()
    # Порог — примерно 1 год
    max_seconds = 365 * 24 * 3600

    # логарифмическая нормализация
    # +1 чтобы избежать log(0)
    ratio = math.log1p(total_seconds) / math.log1p(max_seconds)
    return min(ratio, 1.0)

def ratio2color(ratio, pale):
    if ratio == 0:
        return QtGui.QColor.fromRgb(255, 255, 255)

    # ratio: 0.0 (начало) → 1.0 (конец)
    # HSV: hue = 0 (красный) → 270 (фиолетовый)
    hue = int(270 * (ratio if ratio <= 1. else 1.))
    saturation = 255 if not pale else 50
    value = 255

    return QtGui.QColor.fromHsv(hue, saturation, value)



class Window(QtWidgets.QMainWindow, uic.loadUiType(ChangeExt(sys.argv[0], ".ui"))[0]):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.diagram = DiagramWidget(self)
        self.lo_diagram.addWidget(self.diagram)

        self.files = filesFromFiles(FILES)
        self.files = {f: False for f in self.files}
        self.filesMax = len(self.files)
        self.words, self.ratios, self.expires = {}, {}, {}
        self.filesCur, self.ratioMax, self.ratioCur = 0, 0., 0.

        self.DB_cache = get_all(DB)

        # print("\r\n\r", end="");
        print(".")
        self.newFile()

        self.phase = "Q"
        self.new_word()

    def get_cached(self, q, def_last = None, def_remembered = None):
        def_val = {"last": def_last, "remembered": def_remembered}
        # val = get_value(DB, q, def_val)
        val = self.DB_cache.get(q, def_val)
        return val["last"], val["remembered"]
        
    def set_cached(self, q, last, remembered):
        val = {"last": last, "remembered": remembered}
        self.DB_cache[q] = val
        set_value(DB, q, val)

    def newFile(self):
        if self.filesCur == self.filesMax:
            return

        # for q, exp in self.expires.items():
        #     if exp <= now:
        #         allExpired = False
        #         break

        # profiler = Profiler()
        # profiler.start()

        now = datetime.now()
        for filename, _ in self.files.items():
            if self.files[filename]:
                continue

            for q, a in wordsFromFile(filename).items():
                if q in self.words:
                    if a != self.words[q]:
                        print(f"Duplicate word < {q} > in {filename} : {a} / {self.words[q]}")
                    continue

                self.words[q] = a

                last, remembered = self.get_cached(q, now, timedelta(0))

                expire = last + remembered
                ratio  = timedelta2ratio(remembered)

                self.ratioMax += 1.
                self.ratioCur += ratio

                self.expires[q] = expire
                self.ratios [q] = ratio

            self.filesCur += 1.
            self.files[filename] = True

            print(f"{int(self.ratioMax)} questions after loading {filename}")

            if not self.checkForNewFile():
                break

        # profiler.stop()
        # profiler.open_in_browser()

        self.words = randomDict(self.words)

        self.reindex()

    def reindex(self):
        self.index = sorted(self.ratios, key=self.ratios.get, reverse=True)

    def new_word(self):
        self.current_question = None
        self.current_answer   = None

        now = datetime.now()
        for q, a in self.words.items():
            if self.expires[q] > now:
                continue

            self.last, self.remembered = self.get_cached(q, datetime.now(), timedelta(0))

            self.current_question = q
            self.current_answer   = a
            break

        if self.current_question == None:
            print("All done!")
            self.close()

        self.phase = "Q"
        self.result = 1.
        self.update_view()

    def paintLabel(self, label, ratio):
        palette = label.palette()
        palette.setColor(label.backgroundRole(), ratio2color(ratio, True))
        label.setAutoFillBackground(True)
        label.setPalette(palette)

    def update_view(self):
        if self.current_question:
            self.label_question.setText(self.current_question)
            self.paintLabel(self.label_question, timedelta2ratio(self.remembered))
            self.label_answer  .setText(self.current_answer if self.phase == "A" else "")
            self.label_word.setText(f"{self.last.strftime("%d/%m %H:%M")} | {short_timedelta(self.remembered)}")

    def keyPressEvent(self, event):
        key = event.key()
        mod = event.modifiers()

        if key == Qt.Key_Escape:
            self.close()
        elif self.phase == "Q":
            if key == Qt.Key_Enter or key == Qt.Key_Return or key == Qt.Key_Right:
                self.phase = "A"
                self.update_view()
        elif self.phase == "A":
            ctrl = bool(mod & Qt.ControlModifier)

            plus  = key == Qt.Key_Plus  or key == Qt.Key_Equal or key == Qt.Key_Up
            minus = key == Qt.Key_Minus or key == Qt.Key_Down

            power = 1 if not ctrl else 2
            if   plus :
                self.result = MEMORYUP ** power
            elif minus:
                self.result = 1. / (MEMORYDOWN ** power)

            if self.result != 1.:
                self.store_result()
                self.checkForNewFile()
                self.draw_diagram()
                self.new_word()

    def store_result(self):
        if self.remembered == timedelta(0):
            self.remembered = timedelta(minutes = 1)

        preRemembered = self.remembered

        self.remembered *= self.result

        now = datetime.now()
        self.set_cached(self.current_question, now, self.remembered)

        self.expires[self.current_question] = now + self.remembered

        preRatio = self.ratios [self.current_question]
        self.ratioCur -= preRatio

        ratio = timedelta2ratio(self.remembered)
        self.ratioCur += ratio
        self.ratios [self.current_question] = ratio

        self.reindex()

        self.label_last.setText(f"{self.current_question} = {self.current_answer} | {"+" if self.result > 1. else "-"}  {self.result:.2f} | {preRatio:.2f} > {ratio:.2f} | {short_timedelta(preRemembered)} > {short_timedelta(self.remembered)}")


    def checkForAllExpired(self):
        allExpired = True
        now = datetime.now()
        for q, exp in self.expires.items():
            if exp <= now:
                allExpired = False
                break

        return allExpired

    def checkForNewFile(self):
        if self.checkForAllExpired() or self.ratioCur / self.ratioMax >= WINRATIO:
            self.newFile()

    def draw_diagram(self):
        self.diagram.update()

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = Window()
    window.show()
    sys.exit(app.exec_())
