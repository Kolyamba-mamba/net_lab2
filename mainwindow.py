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
            "work_stream": self.workStreamSpinBox.value(),
            "discipline": self.comboBox.currentText()
        }
                
    def calculate_SLOT(self):
        thingsToShow = modellingSMO(**self.getDataFromUI())
        # удаляем отрисованные графики
        clearLayout(self.graphLayout)
        plt.close('all')
        # рисуем новые
        fig1 = plt.figure()
        ax1 = fig1.add_subplot(111)
        ax1.plot(thingsToShow["statGot"]["x"],thingsToShow["statGot"]["y"], color='blue', label="Всего")
        ax1.plot(thingsToShow["statDone"]["x"],thingsToShow["statDone"]["y"], color='green',  label="Отработанные")
        ax1.plot(thingsToShow["statRefused"]["x"],thingsToShow["statRefused"]["y"], color='red',    label="Отклоненные")
        ax1.legend(loc='upper left', ncol=3)
        addPlotToLayout(fig1, self.graphLayout)
        #fig1.legend(handle1, ["p1", "p2", "p3"], loc='upper left')

        fig2 = plt.figure()
        ax2 = fig2.add_subplot(111)
        ax2.plot(thingsToShow["statQueue"]["x"],thingsToShow["statQueue"]["y"], color='red')
        addPlotToLayout(fig2, self.graphLayout)

        fig3 = plt.figure()
        ax3 = fig3.add_subplot(111)

        test_value = thingsToShow["statWorkflow"]
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
    # import matplotlib.lines as mlines
    space = 0
    # for key_stream in queue:
    #     for request in queue[key_stream]:
    #         # Rectangle((x,y),width,heigth)
    #         #print((request["start"], key_stream+1), request["end"]-request["start"], 1)
    #         x, y = (request["start"], key_stream+1+space)
    #         width, heigth = request["end"]-request["start"], 1
    #         # first variant
    #         rc = Rectangle((x,y),width,heigth, edgecolor = 'blue', facecolor = 'aqua')
    #         plot.add_patch(rc)
    #         # second variant
    #         # l = mlines.Line2D([x,x+width], [y,y])
    #         # plot.add_line(l)
    #         # l = mlines.Line2D([x+width,x+width], [y,y+heigth])
    #         # plot.add_line(l)
    #         # l = mlines.Line2D([x,x+width], [y+heigth,y+heigth])
    #         # plot.add_line(l)
    #         # l = mlines.Line2D([x,x], [y,y+heigth])
    #         # plot.add_line(l)
    #         # third variant
    #         # plot.plot([x, x+width, x+width, x, x], [y, y, y+heigth,y+heigth, y])
        
    #     space += 1

    # four variant
    xarr, yarr, xnextarr, yonearr = [],[],[],[]
    for key_stream in queue:
        for request in queue[key_stream]:
            x, y = (request["start"], key_stream+1+space)
            
            xarr.append(x)
            yarr.append(y)
            xnextarr.append(request["end"])
            yonearr.append(y+1)
        
        space += 1

    plot.vlines(xarr, yarr, yonearr)
    plot.vlines(xnextarr, yarr, yonearr)
    plot.hlines(yarr, xarr, xnextarr)
    plot.hlines(yonearr, xarr, xnextarr)



