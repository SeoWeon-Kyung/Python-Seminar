# PyQt tutorial   URL: https://www.mfitzp.com/tutorials/creating-your-first-pyqt-window/

import pandas as pd
import numpy as np
import matplotlib as plt
import seaborn as sb
from PyQt5.QtWidgets import *
from PyQt5.QtCore import QSize, Qt
from PyQt5.QtGui import *

# main modules : QtWidgets, QtGui, QtCore

import sys

from random import choice

class MainWindow(QMainWindow):
    
    def __init__(self):
        super(MainWindow, self).__init__()

        self.setWindowTitle("My App")

        layout = QGridLayout()

        layout.addWidget(Color('red'), 0, 0)
        layout.addWidget(Color('green'), 1, 0)
        layout.addWidget(Color('blue'), 1, 1)
        layout.addWidget(Color('purple'), 2, 1)

        widget = QWidget()
        widget.setLayout(layout)
        self.setCentralWidget(widget)


class Color(QWidget):
    
    def __init__(self, color):
        super(Color, self).__init__()
        self.setAutoFillBackground(True)

        palette = self.palette()
        palette.setColor(QPalette.Window, QColor(color))
        self.setPalette(palette)
        

app = QApplication(sys.argv)

window = MainWindow()
window.show()

app.exec()