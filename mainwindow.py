from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

from mainwindow_ui import Ui_MainWindow

import matplotlib

matplotlib.use('QT5Agg')

import matplotlib.pylab as plt
import numpy as np


def addPlotToLayout(plot, layout: QLayout):
    from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
    # from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
    layout.addWidget(FigureCanvas(plot))


class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.setupUi(self)

        self.CalcBtn.clicked.connect(self.calculate_SLOT)

    def getDataFromUI(self):
        return {
            "count_requests": self.countRequestSpinBox.value(),
            "input_stream": self.inputStreamSpinBox.value(),
            "queue_length": self.queueLengthSpinBox.value(),
            "request_count": self.countRequestSpinBox.value(),
            "work_stream": self.workStreamSpinBox.value()
        }

    def modellingSMO(self):
        input = self.getDataFromUI()
        queueSize = 0
        currentTime = 0
        requestsGot = 0
        # в начале ни одной заявки нет
        statGot = [[0,0],]
        statDone = [[0,0],]
        statRefused = [[0,0],]
        statQueue = [[0,0],]

        timeNew = self.random(input["input_stream"]) # время, когда придёт новая заявка
        timeDone = None # время, когда текущая заявка будет сделана (None, если заявок пока нет)
        while (requestsGot<input["count_requests"]):
            if (timeDone != None and timeDone <= timeNew): # обслужена очередная заявка
                currentTime = timeDone # переставляем время на время выполнения заявки
                statDone.append([currentTime, statDone[len(statDone)-1]) # добавляем две точки на график
                statDone.append([currentTime, statDone[len(statDone)-1]+1)
                if (queueSize==0):
                    timeDone = None # если очередь пуста, то никто не обслуживается и времени обслуживания нет
                else:
                    queueSize-=1 # в ином случае выполняем следующую заявку
                    timeDone = currentTime + self.random(input["work_stream"])

    def showPlot(self):
        pass

    def calculate_SLOT(self):
        print(self.getDataFromUI())
        
        arr = np.arange(0., 10., 0.5)
        fig, ax1 = plt.subplots()
        ax1.plot(arr)
        addPlotToLayout(fig, self.graphLayout)
