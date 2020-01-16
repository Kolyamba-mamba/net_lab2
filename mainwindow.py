from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

from mainwindow_ui import Ui_MainWindow

import matplotlib

matplotlib.use('QT5Agg')

import matplotlib.pylab as plt
import numpy as np

# ахах какая странная херь
from modeling.modeling import modeling, discipline

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
        self.comboBox.currentIndexChanged.connect(self.onObslChange)
        self.comboBox.setCurrentIndex(0)
        self.onObslChange(0)
        self.onChannelsCountChange(self.channelsSpinBox.value())

        self.comboBox.addItems(discipline)
        self.channelsSpinBox.valueChanged.connect(self.onChannelsCountChange)

    def onObslChange(self, value):
        """
        меняем индексы для того чтоб скрывать части юай
        """
        showRRSetting = value in [2, 6]
        showDRRSetting = value in [6]
        showWeigthSetting = value in [5]
        self.weigthListWdg.setVisible(showWeigthSetting)
        self.stackedWidget.setCurrentIndex(showRRSetting)
        self.stackedWidget1.setCurrentIndex(showDRRSetting)
        

    def makeWeightWidget(self, number):
        widget = QWidget()
        layout = QHBoxLayout()
        layout.addWidget(QLabel(f"приоритет канала {number}"))
        dsb = QDoubleSpinBox()
        dsb.setSingleStep(0.05)
        dsb.setMaximum(1.)
        dsb.setMinimum(0.)
        layout.addWidget(dsb)
        widget.setLayout(layout)
        item = QListWidgetItem(self.weigthListWdg)
        item.setSizeHint(widget.sizeHint())
        self.weigthListWdg.setItemWidget(item, widget)


    def onChannelsCountChange(self, value):
        cnt = self.weigthListWdg.count()
        if cnt > value:
            while self.weigthListWdg.count() > value:
                self.weigthListWdg.takeItem(self.weigthListWdg.count()-1)
        else:
            while self.weigthListWdg.count() < value:
                self.makeWeightWidget(self.weigthListWdg.count()+1)


    def getDataFromUI(self):
        return {
            "discipline": self.comboBox.currentText(),
            "count_channels" : self.channelsSpinBox.value(),
            "count_requests": self.countRequestSpinBox.value(),
            "input_stream": self.inputStreamSpinBox.value(),
            "queue_length": self.queueLengthSpinBox.value(),
            "work_stream": self.workStreamSpinBox.value(),
            "discipline": self.comboBox.currentText(),
            "buffer_size": self.bufferSpinBox.value(),
            "time_quant": self.quantSpinBox.value()
        }
                
    def calculate_SLOT(self):
        dataFromUI = self.getDataFromUI()
        
        thingsToShow = modeling(dataFromUI["discipline"], dataFromUI)

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
        ax1.set_ylabel('Количество заявок')
        ax1.set_xlabel('Время')
        addPlotToLayout(fig1, self.graphLayout)
        #fig1.legend(handle1, ["p1", "p2", "p3"], loc='upper left')

        fig2 = plt.figure()
        ax2 = fig2.add_subplot(111)
        ax2.plot(thingsToShow["statQueue"]["x"],thingsToShow["statQueue"]["y"], color='red', label='Заявок в очереди')
        ax2.legend(loc='upper left', ncol=1)
        ax2.set_ylabel('Очередь')
        ax2.set_xlabel('Время')
        addPlotToLayout(fig2, self.graphLayout)

        fig3 = plt.figure()
        ax3 = fig3.add_subplot(111)
        ax3.set_ylabel('Каналы')
        ax3.set_xlabel('Время')

        statWorkflow = thingsToShow["statWorkflow"]
        drawQueue(ax3, statWorkflow)
        addPlotToLayout(fig3, self.graphLayout)
        # установка ограничений осей
        def search_max_end_stream(stream):
            return max(stream, key = lambda item : item["end"])["end"]

        max_xlim = max([search_max_end_stream(statWorkflow[i]) for i in statWorkflow if len(statWorkflow[i]) != 0])
        ax1.set_xlim(0, max_xlim)
        ax2.set_xlim(0, max_xlim)
        ax3.set_xlim(0, max_xlim)

        ax1.set_ylim(0)
        ax2.set_ylim(0, dataFromUI["queue_length"]+1)
        ax3.set_ylim(0, (max(statWorkflow.keys())+1)*2 + 2)


def drawQueue(plot, queue):
    from pylab import Rectangle
    # import matplotlib.lines as mlines
    space = 0
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



