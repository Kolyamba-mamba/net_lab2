import numpy as np
from collections import deque
from modeling.helper import *

class GPS_simulator:
    def init(self, count_channels, work_stream, weights_dict):
        self.current_time = 0
        self.count_channels = count_channels
        self.work_stream = work_stream
        self.weights_dict = weights_dict

        # очередь
        self.queue = {key: [] for key in range(count_channels)}

        # обслуживаемые заявки
        # вид:
        # { 0: {"name":'t1', "got": 0, "start":0, "end": 7, "channel":, "totalWork":, "done": , "prevStart":},
        #   1: {"name":'t2', "got": 2, "start":2, "end": 11,"channel":, "totalWork":, "done": , "prevStart":} }
        # done — количество выполненной работы
        # totalWork — общее количество работы, нужное для выполнения заявки
        # prevStart — время прошлого пересчёта окончания работы
        self.channels_gps = {key: None for key in range(count_channels)}


    # добавляем заявку на обслуживание
    def addRequest(self, req): 
        if (self.channels_gps[req["channel"]] == None) # текущий канал не обслуживается
            for request in channels_gps:
                if request!=numNew and channels_gps[request]["end"]!=0:
                    el = channels_gps[request]
                    el["done"] += ((el["end"]-el["prevStart"])/el["end"]) * (el["totalWork"]-el["done"])
            
            # пересчитать сроки окончания для gps
            sum_weight = 0
            for i in range(count_channels):
                if channels_gps[i]!=None:
                    sum_weight+=weights_dict[i]
        
            timeDone = None
            for i in range(count_channels):
                el = channels_gps[i]
                el["end"] = currentTime + (el["totalWork"]-el["done"])*weights_dict[i]/sum_weight
                if timeDone==None or el["end"]<timeDone:
                    timeDone = el["end"]
                    numDone = i
        else: # текущий канал обслуживается, ставим в очередь
            (queue[req["channel"]]).append(req)

    # получить имя заявки, которую закончат обслуживать следующей
    def getNext(self):
        pass

    # обслужить следующую заявку
    def serve(self):
        pass

    



def WFQ(input_stream, count_channels, work_stream, queue_length, count_requests, discipline, weights_dict, **kwargs):
    currentTime = 0
    statGot = {'x':[0], 'y':[0]}
    statDone = {'x':[0], 'y':[0]}
    statRefused = {'x':[0], 'y':[0]}
    statQueue = {'x':[0], 'y':[0]}
    curGot = 0
    curDone = 0
    curRefused = 0

    timeNew_arr = {key: random(work_stream) for key in range(count_channels)}
    timeNew_arr[0] = 0

    timeNew = 0 # время, когда придёт новая заявка
    numNew = 0 # номер канала, с которого придёт заявка
    timeDone = None # время, когда будет обслужена следующая заявка
    numDone = None # номер канала, заявку на котором обслужат следующей

    # очередь заявок
    # структура:
    # q(["name":'t1', "got":0, "channel":0],["name":'t2', "got":2, "channel":1])
    queue = []

    # текущее состояние каналов
    # структура channels:
    # { 0: {"name":'t1', "got": 0, "start":0, "end": 7},
    #   1: {"name":'t2', "got": 2, "start":2, "end": 11} }
    # вместо внутреннего словаря будет None, если канал простаивает
    channels = {key: None for key in range(count_channels)}

    # статистика по каналам
    # структура statWorkflow:
    #{  0: [{"name":'t1', "got": 0, "start":0, "end": 7}, {"name": 't3', "got": 5, "start": 7, "end":14}],
    #   1: [{"name":'t2', "got": 2, "start":2, "end": 11}]  }
    # name — название заявки
    # got — время её получения (пока не используется)
    # start — время начала её выполнения
    # end — время конца выполнения
    # ключи списка — номера каналов
    ### -1 канал был убран!

    statWorkflow = {key:[] for key in range(count_channels)}
    # времена получения заявок
    # структура:
    # [{"name":'t4', "got": 6},
    # {"name":'t6', "got": 42}]
    statGotTime = []

    GPS = GPS_simulator()
    GPS.init(count_channels, work_stream, weights_dict)

    while (curGot<count_requests):
        if (timeDone==None or timeNew<timeDone): # сначала поступает заявка
            currentTime = timeNew
            curGot+=1
            addPoint(statGot, currentTime, curGot-1, curGot)
            statGotTime.append({"name":'t'+str(curGot), "got":currentTime})

            GPS.add({"name":'t'+str(curGot), "got":currentTime, "channel":numNew, "totalWork":random(work_stream), "done":0, "end":currentTime, "prevStart":currentTime})
            
            # после добавления новой заявки обновляем время поступления следующей
            timeNew_arr[numNew] = random(input_stream)
            timeNew = timeNew_arr[numNew]
            for el in timeNew_arr:
                if timeNew_arr[el]<timeNew:
                    timeNew=timeNew_arr[el]
                    numNew = el

            freeChannel = None
            for ch in channels:
                if (channels[ch]==None):
                    freeChannel = ch
                    break
            if (freeChannel != None): # если канал свободен, обслуживаем заявку сразу
                timeDone = currentTime + random(work_stream)
                channels[ch] = {"name":'t'+str(curGot), "got": currentTime, "start":currentTime, "end": timeDone}            
            else: # иначе пытаемся добавить в очередь
                if (len(queue)<queue_length):
                    queue.append({"name":'t'+str(curGot), "got": currentTime})
                    addPoint(statQueue, currentTime, len(queue)-1, len(queue))
                else:
                    curRefused += 1
                    addPoint(statRefused, currentTime, curRefused-1, curRefused)
            
        else: # сначала обрабатывается заявка
            currentTime = channels[numDone]["end"]
            statWorkflow.append(channels[numDone])
            curDone+=1
            addPoint(statDone, currentTime, curDone-1 ,curDone)
            if (len(queue)==0): # если очередь пуста, то канал остаётся свободен
                channels[numDone] = None

            else: # в ином случае выполняем следующую заявку
                req_name = GPS.getNext()
                GPS.serve()

                for el in queue:
                    if el["name"]=req_name:
                        req = el
                        break

                queue.remove(req)
                timeDone = currentTime + random(work_stream)
                req["start"] = currentTime
                req["end"] = timeDone
                channels[numDone] = req
                addPoint(statQueue, currentTime, len(queue)+1, len(queue))

            numDone = None
            for ch in channels:
                if channels[ch] != None and (min==None or channels[ch]["end"]<channels[min]["end"]):
                    min = ch

            if numDone == None:
                timeDone = None
            else:
                timeDone = channels["end"]

            
                
                    
            
                