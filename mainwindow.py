from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

from mainwindow_ui import Ui_MainWindow

import matplotlib
matplotlib.use('QT5Agg')

import matplotlib.pylab as plt


def setPlotOnWidget(plot, widget):
    from matplotlib.backends.backend_qt5agg import FigureCanvasQT
    # from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
    # self.plotWidget = FigureCanvas(fig)
    # lay = QtWidgets.QVBoxLayout(self.content_plot)
    # lay.setContentsMargins(0, 0, 0, 0)
    # lay.addWidget(self.plotWidget)
    pass

class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.setupUi(self)

    def getDataFromUI(self):
        pass

    def modellingSMO(self):
        pass

    def showPlot(self):
        pass


