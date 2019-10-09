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
        np.random.seed(1) # удалить после дебага
        super(MainWindow, self).__init__()
        self.setupUi(self)

        self.CalcBtn.clicked.connect(self.calculate_SLOT)

    def getDataFromUI(self):
        return {
            "count_requests": self.countRequestSpinBox.value(),
            "input_stream": self.inputStreamSpinBox.value(),
            "queue_length": self.queueLengthSpinBox.value(),
            "work_stream": self.workStreamSpinBox.value()
        }

    def random(self, scale):
        return np.random.exponential(scale)

    def modellingSMO(self, input):
        queueSize = 0
        currentTime = 0
        requestsGot = 0
        # в начале ни одной заявки нет
        statGot = {'x':[0], 'y':[0]}
        statDone = {'x':[0], 'y':[0]}
        statRefused = {'x':[0], 'y':[0]}
        statQueue = {'x':[0], 'y':[0]}
        curGot = 0
        curDone = 0
        curRefused = 0
        curQueue = 0
        timeNew = self.random(input["input_stream"]) # время, когда придёт новая заявка
        timeDone = None # время, когда текущая заявка будет сделана (None, если заявок пока нет)

        while (requestsGot<input["count_requests"]):
            if (timeDone != None and timeDone <= timeNew): # обслужена очередная заявка
                currentTime = timeDone # переставляем время на время выполнения заявки
                statDone["x"].append(currentTime)   # добавляем точку на график
                statDone["y"].append(curDone)
                curDone+=1
                statDone["x"].append(currentTime)
                statDone["y"].append(curDone)
                if (queueSize==0):
                    timeDone = None # если очередь пуста, то никто не обслуживается и времени обслуживания нет
                else:
                    queueSize-=1 # в ином случае выполняем следующую заявку
                    statQueue["x"].append(currentTime)   # добавляем точку на график
                    statQueue["y"].append(curQueue)
                    curQueue -= 1
                    statQueue["x"].append(currentTime)
                    statQueue["y"].append(curQueue)
                    timeDone = currentTime + self.random(input["work_stream"])
            else: # прибыла новая заявка
                requestsGot+=1
                currentTime = timeNew
                timeNew = currentTime + self.random(input["input_stream"])
                statGot["x"].append(currentTime)   # добавляем точку на график
                statGot["y"].append(curGot)
                curGot+=1
                statGot["x"].append(currentTime)
                statGot["y"].append(curGot)
                if (timeDone==None): # если канал свободен, обслуживаем заявку сразу
                    timeDone = currentTime + self.random(input["work_stream"])
                else: # иначе пытаемся добавить в очередь
                    if (queueSize<input["queue_length"]):
                        queueSize+=1
                        statQueue["x"].append(currentTime)   # добавляем точку на график
                        statQueue["y"].append(curQueue)
                        curQueue+=1
                        statQueue["x"].append(currentTime)
                        statQueue["y"].append(curQueue)
                    else:
                        statRefused["x"].append(currentTime)   # добавляем точку на график
                        statRefused["y"].append(curRefused)
                        curRefused += 1
                        statRefused["x"].append(currentTime)
                        statRefused["y"].append(curRefused)

        # добавляем точки на краю
        statGot["x"].append(currentTime)
        statGot["y"].append(curGot)
        statDone["x"].append(currentTime)
        statDone["y"].append(curDone)
        statRefused["x"].append(currentTime)   
        statRefused["y"].append(curRefused)
        statQueue["x"].append(currentTime)
        statQueue["y"].append(curQueue)
        return [statGot, statDone, statRefused, statQueue]
                

    def showPlot(self):
        pass

    def calculate_SLOT(self):
        input = self.getDataFromUI()
        # print(input)
        # print(self.modellingSMO(input))
        thingsToShow = self.modellingSMO(self.getDataFromUI())

        fig1 = plt.figure()
        ax = fig1.add_subplot(111)
        ax.plot(thingsToShow[0]["x"],thingsToShow[0]["y"], color='yellow')
        ax.plot(thingsToShow[1]["x"],thingsToShow[1]["y"], color='green')
        ax.plot(thingsToShow[2]["x"],thingsToShow[2]["y"], color='red')
        addPlotToLayout(fig1, self.graphLayout)

        fig2 = plt.figure()
        ax2 = fig2.add_subplot(111)
        ax2.plot(thingsToShow[3]["x"],thingsToShow[3]["y"], color='red')
        addPlotToLayout(fig2, self.graphLayout)





