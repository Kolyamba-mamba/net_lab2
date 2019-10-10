import numpy as np
from collections import deque

def random(scale):
    return np.random.exponential(1/scale)

def modellingSMO(input):
    currentTime = 0
    # в начале ни одной заявки нет
    statGot = {'x':[0], 'y':[0]}
    statDone = {'x':[0], 'y':[0]}
    statRefused = {'x':[0], 'y':[0]}
    statQueue = {'x':[0], 'y':[0]}
    curGot = 0
    curDone = 0
    curRefused = 0
    timeNew = random(input["input_stream"]) # время, когда придёт новая заявка (можно заменить на 0)

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
            if channels[ch] != None:
                min = True
        if (min):
            for ch in channels: 
                if (channels[ch]!=None and channels[ch]["end"]<timeNew and (min==True or channels[ch]["end"]<min)):
                    min = ch

        if (min!=None and min!=True): # обслужена очередная заявка
            currentTime = channels[min]["end"] # переставляем время на время выполнения заявки
            statWorkflow[min].append(channels[min])
            statDone["x"].append(currentTime)   # добавляем точку на график
            statDone["y"].append(curDone)
            curDone+=1
            statDone["x"].append(currentTime)
            statDone["y"].append(curDone)
            if (queue.__len__()==0): # если очередь пуста, то канал остаётся свободен
                channels[min] = None
            else: # в ином случае выполняем следующую заявку
                r = queue.popleft()
                timeDone = currentTime + random(input["work_stream"])
                channels[min] = {"name":r["name"], "got": r["got"], "start":currentTime, "end": timeDone}
                statQueue["x"].append(currentTime)   # добавляем точку на график
                statQueue["y"].append(queue.__len__()+1)
                statQueue["x"].append(currentTime)
                statQueue["y"].append(queue.__len__())
        else: # прибыла новая заявка
            currentTime = timeNew
            timeNew = currentTime + random(input["input_stream"])
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
                timeDone = currentTime + random(input["work_stream"])
                channels[ch] = {"name":'t'+str(curGot), "got": currentTime, "start":currentTime, "end": timeDone}            
            else: # иначе пытаемся добавить в очередь
                if (queue.__len__()<input["queue_length"]):
                    queue.append({"name":'t'+str(curGot), "got": currentTime})
                    statQueue["x"].append(currentTime)   # добавляем точку на график
                    statQueue["y"].append(queue.__len__()-1)
                    statQueue["x"].append(currentTime)
                    statQueue["y"].append(queue.__len__())
                else:
                    statWorkflow[-1].append({"name":'t'+str(curGot), "got":currentTime, "start":currentTime, "end":currentTime})
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