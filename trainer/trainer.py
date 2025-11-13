# from pyinstrument import Profiler

import math
from datetime import datetime, timedelta

from PyQt5 import QtWidgets, uic, QtGui
from PyQt5.QtCore import Qt, QRectF

import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../python/'))) # Добавляем в sys.path путь к папке python
from common import wordsFrom, randomDict, filesFromFiles, wordsFromFile
from common_db import set_value, get_value

# THEME = "lex"
# FILES = f"./source/{THEME}.files"
THEME = "course"
FILES = f"./course/{THEME}.files"
DB  = f"./trainer/{THEME}.db"

MEMORYUP   = 2.5
MEMORYDOWN = 3.0
WINRATIO = 0.6

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

        # wnd.label_files.setText(f"{int(wnd.filesCur)} / {int(wnd.filesMax)} | {filesExp} / {int(wnd.ratioMax)} | {wnd.ratioCur / wnd.ratioMax:.5f}")

        # print(f"{wnd.ratioCur:.2f} / {int(wnd.ratioMax)} = {wnd.ratioCur / wnd.ratioMax:.5f}")
        wnd.label_total.setText(f"remembered {wnd.ratioCur:.2f} / {int(wnd.ratioMax)}")
        wnd.paintLabel(wnd.label_total, wnd.ratioCur / wnd.ratioMax)

        # print(f"{int(wnd.filesCur)} / {int(wnd.filesMax)} = {wnd.filesCur / wnd.filesMax:.5f}")
        wnd.label_files.setText(f"files {int(wnd.filesCur)} / {int(wnd.filesMax)}")
        wnd.paintLabel(wnd.label_files, wnd.filesCur / wnd.filesMax)

        # print(f"{int(filesExp)} / {int(wnd.ratioMax)} = {filesExp / wnd.ratioMax:.5f}")
        wnd.label_words.setText(f"learned {int(filesExp)} / {int(wnd.ratioMax)}")
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
        self.filesCur, self.ratioMax, self.ratioCur = 0., 0., 0.

        # print("\r\n\r", end="");
        print(".")
        self.newFile()

        self.phase = "Q"
        self.new_word()

    def newFile(self):
        if self.filesCur == self.filesMax:
            return

        now = datetime.now()
        for filename, _ in self.files.items():
            if self.files[filename]:
                continue

            for q, a in wordsFromFile(filename).items():
                if q in self.words and a != self.words[q]:
                    print(f"Duplicate word <{q}> in {filename}")
                    continue

                self.words[q] = a

                word_data = get_value(DB, q)
                remembered = word_data.get("remembered") if word_data else timedelta(0)
                last       = word_data.get("last")       if word_data else now

                expire = last + remembered
                ratio  = timedelta2ratio(remembered)

                self.ratioMax += 1.
                self.ratioCur += ratio

                self.expires[q] = expire
                self.ratios [q] = ratio

            self.filesCur += 1.
            self.files[filename] = True

            # print(self.ratioMax, self.ratioCur, self.ratioCur / self.ratioMax, filename)
            print(f"{int(self.ratioMax)} questions after loading {filename}")

            if self.ratioCur / self.ratioMax < WINRATIO:
                break

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

            def_val = {"last": datetime.now(), "remembered": timedelta(0)}
            word_data = get_value(DB, q, def_val)
            self.last       = word_data.get("last")
            self.remembered = word_data.get("remembered")

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
            ctrl = mod & Qt.ControlModifier

            plus  = key == Qt.Key_Plus  or key == Qt.Key_Equal or key == Qt.Key_Up
            minus = key == Qt.Key_Minus or key == Qt.Key_Down
            if ctrl and plus:
                self.result = MEMORYUP * MEMORYUP * MEMORYUP
            elif ctrl and minus:
                self.result = 1 / (MEMORYDOWN * MEMORYDOWN * MEMORYDOWN)
            elif plus:
                self.result = MEMORYUP
            elif minus:
                self.result = 1 / MEMORYDOWN

            if self.result != 1.:

                # profiler = Profiler()
                # profiler.start()

                self.store_result()
                self.draw_diagram()
                self.new_word()

                # profiler.stop()
                # profiler.open_in_browser()

    def store_result(self):
        if self.remembered == timedelta(0):
            self.remembered = timedelta(minutes = 5)

        self.remembered *= self.result

        now = datetime.now()
        set_value(DB, self.current_question, {"last": now, "remembered": self.remembered})

        self.expires[self.current_question] = now + self.remembered

        ratio = self.ratios [self.current_question]
        self.ratioCur -= ratio

        ratio = timedelta2ratio(self.remembered)
        self.ratioCur += ratio
        self.ratios [self.current_question] = ratio

        self.reindex()

        if self.ratioCur / self.ratioMax >= WINRATIO:
            self.newFile()


    def draw_diagram(self):
        self.diagram.update()

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = Window()
    window.show()
    sys.exit(app.exec_())
