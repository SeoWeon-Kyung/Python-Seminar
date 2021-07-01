# PyQt tutorial   URL: https://www.mfitzp.com/tutorials/creating-your-first-pyqt-window/

import pandas as pd
import numpy as np
import matplotlib as plt
import seaborn as sb
from PyQt5.QtWidgets import *
from PyQt5.QtCore import QSize, Qt

# main modules : QtWidgets, QtGui, QtCore

import sys

from random import choice


class MainWindow(QMainWindow):
    
    def __init__(self):
        super(MainWindow, self).__init__()

        self.setWindowTitle("My App")

        widget = QComboBox()
        widget.addItems(["One", "Two", "Three"])

        # Sends the current index (position) of the selected item.
        widget.currentIndexChanged.connect( self.index_changed )

        # There is an alternate signal to send the text.
        widget.editTextChanged.connect( self.text_changed )

        self.setCentralWidget(widget)


    def index_changed(self, i): # i is an int
        print(i)

    def text_changed(self, s): # s is a str
        print(s)
        

app = QApplication(sys.argv)

window = MainWindow()
window.show()

app.exec()