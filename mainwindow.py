from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

from mainwindow_ui import Ui_MainWindow

import matplotlib

matplotlib.use('QT5Agg')

import matplotlib.pylab as plt
import numpy as np
from collections import deque


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
            "channels" : self.channelsSpinBox.value(),
            "count_requests": self.countRequestSpinBox.value(),
            "input_stream": self.inputStreamSpinBox.value(),
            "queue_length": self.queueLengthSpinBox.value(),
            "work_stream": self.workStreamSpinBox.value()
        }

    def random(self, scale):
        return np.random.exponential(scale)

    def modellingSMO(self, input):
        currentTime = 0
        # в начале ни одной заявки нет
        statGot = {'x':[0], 'y':[0]}
        statDone = {'x':[0], 'y':[0]}
        statRefused = {'x':[0], 'y':[0]}
        statQueue = {'x':[0], 'y':[0]}
        curGot = 0
        curDone = 0
        curRefused = 0
        timeNew = self.random(input["input_stream"]) # время, когда придёт новая заявка (можно заменить на 0)

        # очередь заявок
        # структура:
        # q(["name":'t1', "got":0],["name":'t2', "got":2])
        queue = deque() #append, popleft, count

        # текущее состояние каналов
        # структура channels:
        # { 0: {"name":'t1', "got": 0, "start":0, "end": 7},
        #   1: {"name":'t2', "got": 2, "start":2, "end": 11} }
        # вместо внутреннего словаря будет None, если канал простаивает
        channels = {key: None for key in range(input["channels"])}

        # статистика по каналам
        # структура statWorkflow:
        #{ -1: [{"name":'t4', "got": 6}]
        #   0: [{"name":'t1', "got": 0, "start":0, "end": 7}, {"name": 't3', "got": 5, "start": 7, "end":14}],
        #   1: [{"name":'t2', "got": 2, "start":2, "end": 11}]  }
        # name — название заявки
        # got — время её получения
        # start — время начала её выполнения
        # end — время конца выполнения
        # ключи списка — номера каналов, -1 — канал отброшенных заявок
        statWorkflow = {key:[] for key in range(-1, input["channels"])}
        

        while (curGot<input["count_requests"]):
            min = None
            # находим наиболее быстро обслуженную заявку и сравниваем с временем поступления новой
            for ch in channels: 
                if ((channels[ch] != None) and (min==None or channels[ch]["time"]<timeNew or channels[ch]["time"]<min)):
                    min = ch

            if (min!=None): # обслужена очередная заявка
                currentTime = channels[min]["end"] # переставляем время на время выполнения заявки
                statWorkflow[min].append(channels[min])
                statDone["x"].append(currentTime)   # добавляем точку на график
                statDone["y"].append(curDone)
                curDone+=1
                statDone["x"].append(currentTime)
                statDone["y"].append(curDone)
                if (queue.__len__()==0):
                    channels[min] = None
                else: # в ином случае выполняем следующую заявку
                    r = queue.popleft()
                    timeDone = currentTime + self.random(input["work_stream"])
                    channels[min] = {"name":r.name, "got": r.got, "start":currentTime, "end": timeDone}
                    statQueue["x"].append(currentTime)   # добавляем точку на график
                    statQueue["y"].append(queue.count()+1)
                    statQueue["x"].append(currentTime)
                    statQueue["y"].append(queue.count())
            else: # прибыла новая заявка
                currentTime = timeNew
                timeNew = currentTime + self.random(input["input_stream"])
                statGot["x"].append(currentTime)   # добавляем точку на график
                statGot["y"].append(curGot)
                curGot+=1
                statGot["x"].append(currentTime)
                statGot["y"].append(curGot)
                freeChannel = None
                for ch in channels:
                    if (channels[ch]==None):
                        freeChannel = ch
                        break
                if (freeChannel != None): # если канал свободен, обслуживаем заявку сразу
                    timeDone = currentTime + self.random(input["work_stream"])
                    channels[ch] = {"name":'t'+str(curGot), "got": currentTime, "start":currentTime, "end": timeDone}            
                else: # иначе пытаемся добавить в очередь
                    if (queue.__len__()<input["queue_length"]):
                        queue.append({"name":'t'+str(curGot), "got": currentTime})
                        statQueue["x"].append(currentTime)   # добавляем точку на график
                        statQueue["y"].append(queue.__len__()-1)
                        statQueue["x"].append(currentTime)
                        statQueue["y"].append(queue.__len__())
                    else:
                        statWorkflow[-1].append({"name":'t'+str(curGot), "got":currentTime})
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
        statQueue["y"].append(queue.__len__())
        return [statGot, statDone, statRefused, statQueue, statWorkflow]
                
    def calculate_SLOT(self):
        # print(input)
        # print(self.modellingSMO(input))
        thingsToShow = self.modellingSMO(self.getDataFromUI())
        
        clearLayout(self.graphLayout)
        plt.close('all')

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





