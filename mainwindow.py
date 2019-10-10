from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

from mainwindow_ui import Ui_MainWindow

import matplotlib

matplotlib.use('QT5Agg')

import matplotlib.pylab as plt
import numpy as np

from modelling import modellingSMO


def addPlotToLayout(plot, layout: QLayout):
    from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
    # from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
    layout.addWidget(FigureCanvas(plot))

def clearLayout(layout: QLayout):
    for i in reversed(range(layout.count())):
        layout.removeItem(layout.itemAt(i))



class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self):
        np.random.seed(1) # удалить после дебага
        super(MainWindow, self).__init__()
        self.setupUi(self)

        self.CalcBtn.clicked.connect(self.calculate_SLOT)

    def getDataFromUI(self):
        return {
            "count_channels" : self.channelsSpinBox.value(),
            "count_requests": self.countRequestSpinBox.value(),
            "input_stream": self.inputStreamSpinBox.value(),
            "queue_length": self.queueLengthSpinBox.value(),
            "work_stream": self.workStreamSpinBox.value()
        }
                
    def calculate_SLOT(self):
        thingsToShow = modellingSMO(**self.getDataFromUI())
        # удаляем отрисованные графики
        clearLayout(self.graphLayout)
        plt.close('all')
        # рисуем новые
        fig1 = plt.figure()
        ax1 = fig1.add_subplot(111)
        ax1.plot(thingsToShow[0]["x"],thingsToShow[0]["y"], color='blue', label="Всего")
        ax1.plot(thingsToShow[1]["x"],thingsToShow[1]["y"], color='green',  label="Отработанные")
        ax1.plot(thingsToShow[2]["x"],thingsToShow[2]["y"], color='red',    label="Отклоненные")
        ax1.legend(loc='upper left', ncol=3)
        addPlotToLayout(fig1, self.graphLayout)

        fig2 = plt.figure()
        ax2 = fig2.add_subplot(111)
        ax2.plot(thingsToShow[3]["x"],thingsToShow[3]["y"], color='red')
        addPlotToLayout(fig2, self.graphLayout)

        fig3 = plt.figure()
        ax3 = fig3.add_subplot(111)

        test_value = thingsToShow[4]
        drawQueue(ax3, test_value)
        addPlotToLayout(fig3, self.graphLayout)
        # установка ограничений осей
        def search_max_end_stream(stream):
            return max(stream, key = lambda item : item["end"])["end"]

        max_xlim = max([search_max_end_stream(test_value[i]) for i in test_value if len(test_value[i]) != 0])
        ax1.set_xlim(0, max_xlim)
        ax2.set_xlim(0, max_xlim)
        ax3.set_xlim(0, max_xlim)

        ax1.set_ylim(0)
        ax2.set_ylim(0)
        ax3.set_ylim(0, (max(test_value.keys())+1)*2 + 2)


def drawQueue(plot, queue):
    from pylab import Rectangle

    space = 0
    for key_stream in queue:
        for request in queue[key_stream]:
            # Rectangle((x,y),width,heigth)
            #print((request["start"], key_stream+1), request["end"]-request["start"], 1)
            rc = Rectangle((request["start"], key_stream+1+space), request["end"]-request["start"], 1, edgecolor = 'blue', facecolor = 'aqua')
            plot.add_patch(rc)
        
        space += 1



