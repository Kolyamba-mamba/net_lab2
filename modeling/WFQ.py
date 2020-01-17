import numpy as np
from collections import deque
from modeling.helper import *
from modeling.gps import *


def WFQ(input_stream, count_channels, work_stream, queue_length, count_requests, discipline, weights_dict, **kwargs):
    currentTime = 0
    statGot = {'x': [0], 'y': [0]}
    statDone = {'x': [0], 'y': [0]}
    statRefused = {'x': [0], 'y': [0]}
    statQueue = {'x': [0], 'y': [0]}
    curGot = 0
    curDone = 0
    curRefused = 0

    # массив времён поступления заявок с разных каналов
    timeNew_arr = {key: random(work_stream) for key in range(count_channels)}
    timeNew_arr[0] = 0

    timeNew = 0  # время, когда придёт новая заявка
    numNew = 0  # номер канала, с которого придёт заявка
    timeDone = None  # время, когда будет обслужена следующая заявка

    # очередь заявок
    # структура:
    # q(["name":'t1', "got":0, "channel":0],["name":'t2', "got":2, "channel":1])
    queue = []

    # текущее состояние каналов
    # структура channels:
    # {"name":'t1', "got": 0, "start":0, "end": 7}
    # вместо внутреннего словаря будет None, если канал простаивает
    channel = {}

    # статистика по каналам
    # структура statWorkflow:
    # {  0: [{"name":'t1', "got": 0, "start":0, "end": 7}, {"name": 't3', "got": 5, "start": 7, "end":14}],
    #   1: [{"name":'t2', "got": 2, "start":2, "end": 11}]  }
    # name — название заявки
    # got — время её получения (пока не используется)
    # start — время начала её выполнения
    # end — время конца выполнения
    # ключи списка — номера каналов
    ### -1 канал был убран!
    statWorkflow = {key: [] for key in range(count_channels)}

    # времена получения заявок
    # структура:
    # [{"name":'t4', "got": 6},
    # {"name":'t6', "got": 42}]
    statGotTime = []

    GPS = GPS_simulator(count_channels, weights_dict)

    while curGot < count_requests:
        if timeDone is None or timeNew < timeDone:  # сначала поступает заявка
            currentTime = timeNew
            curGot += 1
            addPoint(statGot, currentTime, curGot - 1, curGot)
            statGotTime.append({"name": 't' + str(curGot), "got": currentTime})

            GPS.addRequest({"name": 't' + str(curGot), "got": currentTime, "channel": numNew, "totalWork": random(work_stream),
                     "done": 0, "end": currentTime, "prevStart": currentTime})

            if channel == {}:  # если канал свободен, обслуживаем заявку сразу
                timeDone = currentTime + random(work_stream)
                channel = {"name": 't' + str(curGot), "got": currentTime, "start": currentTime, "end": timeDone, "channel":numNew}
            else:  # иначе пытаемся добавить в очередь
                if len(queue) < queue_length:
                    queue.append({"name": 't' + str(curGot), "got": currentTime, "channel":numNew})
                    addPoint(statQueue, currentTime, len(queue) - 1, len(queue))
                else:
                    curRefused += 1
                    addPoint(statRefused, currentTime, curRefused - 1, curRefused)

            # после добавления новой заявки обновляем время поступления следующей
            timeNew_arr[numNew] = random(input_stream)
            timeNew = timeNew_arr[numNew]
            for el in range(len(timeNew_arr)):
                if timeNew_arr[el] < timeNew:
                    timeNew = timeNew_arr[el]
                    numNew = el

        else:  # сначала обрабатывается заявка
            currentTime = channel["end"]

            statWorkflow[channel["channel"]].append(channel)
            curDone += 1
            addPoint(statDone, currentTime, curDone - 1, curDone)
            if len(queue) == 0:  # если очередь пуста, то канал остаётся свободен
                channel = {}

            else:  # в ином случае выполняем следующую заявку
                req_name = GPS.getNext()
                if (req_name != None):
                    req = None
                    # цикл для ситуаций, когда элемент с таким именем не в очереди, а уже обрабатывается
                    # такие элементы пропускаются
                    while req is None and req_name is not None: 
                        req_name = GPS.getNext()
                        print(req_name)
                        print(queue)
                        if req_name is None:
                            break
                        GPS.serve()
                        for el in queue:
                            if el["name"] == req_name:
                                req = el
                                break
                
                    if req_name is not None:
                        queue.remove(req)
                        timeDone = currentTime + random(work_stream)
                        req["start"] = currentTime
                        req["end"] = timeDone
                        channel = req
                        addPoint(statQueue, currentTime, len(queue) + 1, len(queue))

            if channel != {}:
                timeDone = None
            else:
                timeDone = channel["end"]
                
    # добавляем точки на краю
    addPoint(statGot, currentTime, curGot, curGot)
    addPoint(statDone, currentTime, curDone, curDone)
    addPoint(statRefused, currentTime, curRefused, curRefused)
    addPoint(statQueue, currentTime, len(queue), len(queue))
    print("statWorkflow: ", statWorkflow)

    return {
        "statGot":statGot,
        "statDone":statDone,
        "statRefused":statRefused,
        "statQueue":statQueue,
        "statWorkflow":statWorkflow,
        "statGotTime":statGotTime
    }
