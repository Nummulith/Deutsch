import sys
import random
from datetime import timedelta
from PyQt5 import QtWidgets, QtGui, QtCore


class DiagramWidget(QtWidgets.QWidget):
    def __init__(self, words):
        super().__init__()
        self.words = words
        self.setMinimumSize(400, 300)

    def paintEvent(self, event):
        qp = QtGui.QPainter(self)
        qp.setRenderHint(QtGui.QPainter.Antialiasing)

        w, h = self.width(), self.height()
        cols = int(len(self.words) ** 0.5) or 1
        size = min(w // cols, h // cols)

        for i, (word, remembered) in enumerate(self.words):
            x = (i % cols) * size
            y = (i // cols) * size
            color = self.color_from_timedelta(remembered)
            qp.fillRect(x, y, size - 2, size - 2, color)

        qp.end()

    def color_from_timedelta(self, td: timedelta):
        """Преобразует timedelta в цвет от красного до фиолетового"""
        # Преобразуем в секунды, нормализуем в диапазон 0..1 (0 = 0 сек, 1 = 100 лет)
        total_seconds = td.total_seconds()
        max_seconds = 100 * 365 * 24 * 3600  # 100 лет
        ratio = min(total_seconds / max_seconds, 1.0)

        # Плавный переход от красного (0) к фиолетовому (1)
        # Красный = (255, 0, 0), Фиолетовый = (128, 0, 255)
        r = int(255 - 127 * ratio)
        g = 0
        b = int(255 * ratio)
        return QtGui.QColor(r, g, b)


class Window(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Word Memory Diagram")

        # тестовые данные
        self.words = [
            ("apple", timedelta(seconds=0)),
            ("banana", timedelta(days=1)),
            ("cherry", timedelta(days=10)),
            ("date", timedelta(days=100)),
            ("elderberry", timedelta(days=1000)),
            ("fig", timedelta(days=3650)),  # ~10 лет
            ("grape", timedelta(days=36500)),  # ~100 лет
        ]

        self.widget = DiagramWidget(self.words)
        self.setCentralWidget(self.widget)


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    win = Window()
    win.resize(500, 400)
    win.show()
    sys.exit(app.exec_())
