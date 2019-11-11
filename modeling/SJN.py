from heapq import *
from modeling.helper import *


def getNextRequest(container: list):
    res = heappop(container)
    return {
        "name": res.name,
        "got": res.got,
        "work": res.work
    }
    

class Point():
    def __init__(self, name, got, work):
        self.name = name
        self.got = got
        self.work = work
    
    def __it__(self, other):
        return self.work < other.work

    def __gt__(self, other):
        return self.work > other.work



def SJN(input_stream, count_channels, work_stream, queue_length, count_requests, discipline, **kwargs):
    currentTime = 0
    # в начале ни одной заявки нет
    statGot = {'x':[0], 'y':[0]}
    statDone = {'x':[0], 'y':[0]}
    statRefused = {'x':[0], 'y':[0]}
    statQueue = {'x':[0], 'y':[0]}
    curGot = 0
    curDone = 0
    curRefused = 0
    timeNew = random(input_stream) # время, когда придёт новая заявка (можно заменить на 0)

    # очередь заявок
    # структура:
    # q(["name":'t1', "got":0],["name":'t2', "got":2])
    queue = []

    # текущее состояние каналов
    # структура channels:
    # { 0: {"name":'t1', "got": 0, "start":0, "end": 7},
    #   1: {"name":'t2', "got": 2, "start":2, "end": 11} }
    # вместо внутреннего словаря будет None, если канал простаивает
    channels = {key: None for key in range(count_channels)}

    # статистика по каналам
    # структура statWorkflow:
    #{ -1: [{"name":'t4', "got": 6}]
    #   0: [{"name":'t1', "got": 0, "start":0, "end": 7}, {"name": 't3', "got": 5, "start": 7, "end":14}],
    #   1: [{"name":'t2', "got": 2, "start":2, "end": 11}]  }
    # name — название заявки
    # got — время её получения (пока не используется)
    # start — время начала её выполнения
    # end — время конца выполнения
    # ключи списка — номера каналов
    ### -1 канал был убран!
    statWorkflow = {key:[] for key in range(count_channels)}
    # времена получения заявок
    # структура:
    # [{"name":'t4', "got": 6},
    # {"name":'t6', "got": 42}]
    statGotTime = []


    while (curGot<count_requests):
        min = None
        # находим наиболее быстро обслуженную заявку и сравниваем с временем поступления новой
        for ch in channels:
            if channels[ch] != None and channels[ch]["end"]<timeNew and (min==None or channels[ch]["end"]<channels[min]["end"]):
                min = ch

        if (min != None): # обслужена очередная заявка
            currentTime = channels[min]["end"] # переставляем время на время выполнения заявки
            statWorkflow[min].append(channels[min])
            curDone+=1
            addPoint(statDone, currentTime, curDone-1 ,curDone)
            if (len(queue)==0): # если очередь пуста, то канал остаётся свободен
                channels[min] = None
            else: # в ином случае выполняем следующую заявку
                r = getNextRequest(queue)
                timeDone = currentTime + r["work"]
                channels[min] = {"name":r["name"], "got": r["got"], "start":currentTime, "end": timeDone}
                addPoint(statQueue, currentTime, len(queue)+1, len(queue))
        else: # прибыла новая заявка
            currentTime = timeNew
            timeNew = currentTime + random(input_stream)
            curGot+=1
            addPoint(statGot, currentTime, curGot-1, curGot)
            statGotTime.append({"name":'t'+str(curGot), "got":currentTime})
            freeChannel = None
            for ch in channels:
                if (channels[ch]==None):
                    freeChannel = ch
                    break
            if (freeChannel != None): # если канал свободен, обслуживаем заявку сразу
                timeDone = currentTime + random(work_stream)
                channels[ch] = {"name":'t'+str(curGot), "got": currentTime, "start":currentTime, "end": timeDone}            
            else:
                if (len(queue)<queue_length):
                    heappush(queue, Point('t'+str(curGot), currentTime, random(work_stream)))
                    addPoint(statQueue, currentTime, len(queue)-1, len(queue))
                else:
                    queue.pop()
                    curRefused += 1
                    addPoint(statRefused, currentTime, curRefused-1, curRefused)

    # добавляем точки на краю
    addPoint(statGot, currentTime, curGot, curGot)
    addPoint(statDone, currentTime, curDone, curDone)
    addPoint(statRefused, currentTime, curRefused, curRefused)
    addPoint(statQueue, currentTime, len(queue), len(queue))

    return {
        "statGot":statGot,
        "statDone":statDone,
        "statRefused":statRefused,
        "statQueue":statQueue,
        "statWorkflow":statWorkflow,
        "statGotTime":statGotTime
    }