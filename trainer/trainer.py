import sys
import os
import math
from datetime import datetime, timedelta

from PyQt5 import QtWidgets, uic, QtGui
from PyQt5.QtCore import Qt, QRectF

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../python/'))) # Добавляем в sys.path путь к папке python
from common import wordsFromCfg, randomDict
from common_db import set_value, get_value

theme = "course"
# CFG = f"./source/{theme}.files"
CFG = f"./course/{theme}.files"
DB  = f"./trainer/{theme}.db"

memoryK = 2.5

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
        qp = QtGui.QPainter(self)
        qp.setRenderHint(QtGui.QPainter.Antialiasing)

        words = self.window.index
        n = len(words)
        if n == 0:
            return

        w, h = self.width(), self.height()

        # вычисляем число колонок так, чтобы квадраты целиком влезли по вертикали
        cols = int((w / h * n) ** 0.5) or 1
        rows = (n + cols - 1) // cols

        # вычисляем размер квадрата
        size = min(w / cols, h / rows)

        # если есть "лишнее" пространство — не центрируем, просто обрезаем
        for i, q in enumerate(words):
            col = i % cols
            row = i // cols
            x = col * size
            y = row * size
            if y >= h:  # за границей формы — не рисуем
                break
            ratio = self.window.ratios[q]
            qp.fillRect(QRectF(x, y, size, size), ratio2color(ratio))

        qp.end()

def timedelta2ratio(td: timedelta):
    total_seconds = td.total_seconds()
    # Порог — примерно 1 год
    max_seconds = 365 * 24 * 3600

    # логарифмическая нормализация
    # +1 чтобы избежать log(0)
    ratio = math.log1p(total_seconds) / math.log1p(max_seconds)
    return min(ratio, 1.0)

def ratio2color(ratio):
    # ratio: 0.0 (начало) → 1.0 (конец)
    # HSV: hue = 0 (красный) → 270 (фиолетовый)
    hue = int(360 * ratio)  # можно сделать 360, если хочешь полный круг
    saturation = 255
    value = 255
    return QtGui.QColor.fromHsv(hue, saturation, value)

class Window(QtWidgets.QMainWindow, uic.loadUiType(ChangeExt(sys.argv[0], ".ui"))[0]):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.words = randomDict(wordsFromCfg(CFG))

        self.ratios = {}
        for i, (q, a) in enumerate(self.words.items()):
            print(".", end="", flush=True)
            word_data = get_value(DB, q)
            remembered = word_data.get("remembered") if word_data else timedelta(0)
            self.ratios[q] = timedelta2ratio(remembered)
        print("!")
        self.reindex()

        self.diagram = DiagramWidget(self)
        self.verticalLayout.addWidget(self.diagram)

        self.phase = "Q"
        self.new_word()

    def reindex(self):
        self.index = sorted(self.ratios, key=self.ratios.get, reverse=True)

    def new_word(self):
        self.current_question = None
        self.current_answer   = None

        for q, a in self.words.items():
            def_val = {"last": datetime.now(), "remembered": timedelta(0)}
            word_data = get_value(DB, q, def_val)
            self.last       = word_data.get("last")
            self.remembered = word_data.get("remembered")

            if self.last + self.remembered > datetime.now():
                continue

            self.current_question = q
            self.current_answer   = a
            break

        if self.current_question == None:
            print("All done!")
            self.close()

        self.phase = "Q"
        self.result = 1.
        self.update_view()

    def update_view(self):
        self.label_question.setText(self.current_question)
        self.label_answer  .setText(self.current_answer if self.phase == "A" else "")
        self.label_info    .setText(f"{self.last.strftime("%d/%m %H:%M")} | {short_timedelta(self.remembered)}")

    def keyPressEvent(self, event):
        key = event.key()
        mod = event.modifiers()

        if key == Qt.Key_Escape:
            self.close()
        elif self.phase == "Q":
            if key == Qt.Key_Enter:
                self.phase = "A"
                self.update_view()
        elif self.phase == "A":
            ctrl = mod & Qt.ControlModifier

            if ctrl and (key == Qt.Key_Plus or key == Qt.Key_Equal):  # Ctrl + "+"
                self.result = memoryK * memoryK * memoryK
            elif ctrl and key == Qt.Key_Minus:                       # Ctrl + "-"
                self.result = 1 / (memoryK * memoryK * memoryK)
            elif key == Qt.Key_Plus or key == Qt.Key_Equal:  # + на разных клавиатурах
                self.result = memoryK
            elif key == Qt.Key_Minus:
                self.result = 1 / memoryK

            if self.result != 1.:
                self.store_result()
                self.draw_diagram()
                self.new_word()

    def store_result(self):
        if self.remembered == timedelta(0):
            self.remembered = timedelta(minutes = 5)

        self.remembered *= self.result

        set_value(DB, self.current_question, {"last": datetime.now(), "remembered": self.remembered})

        self.ratios[self.current_question] = timedelta2ratio(self.remembered)
        self.reindex()

    def draw_diagram(self):
        self.diagram.update()

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = Window()
    window.show()
    sys.exit(app.exec_())
