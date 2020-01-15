
import numpy as np
from collections import deque
from modeling.helper import *

def CSWFQ(input_stream, count_channels, work_stream, queue_length, count_requests, discipline, weights_dict, **kwargs):
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
    # q(["name":'t1', "got":0, "left":10],["name":'t2', "got":2, "left":7])
    queue = deque() #append, popleft, count

    buffer = deque()

    # текущее состояние каналов
    # структура channels:
    # { 0: {"name":'t1', "got": 0, "start":0, "end": 7, "left":10},
    #   1: {"name":'t2', "got": 2, "start":2, "end": 11, "left":7} }
    # вместо внутреннего словаря будет None, если канал простаивает
    channels = {key: None for key in range(count_channels)}

    # статистика по каналам
    # структура statWorkflow:
    #{  0: [{"name":'t1', "got": 0, "start":0, "end": 7, "left":10}, {"name": 't3', "got": 5, "start": 7, "end":14, "left":10}],
    #   1: [{"name":'t2', "got": 2, "start":2, "end": 11, "left":10}]  }
    # name — название заявки
    # got — время её получения (пока не используется)
    # start — время начала её выполнения
    # end — время конца выполнения
    # left — оставшееся время для обслуживания заявки
    # ключи списка — номера каналов
    statWorkflow = {key:[] for key in range(count_channels)}
    # времена получения заявок
    # структура:
    # [{"name":'t4', "got": 6},
    # {"name":'t6', "got": 42}]
    statGotTime = []

    lastReq = 0

    while (curGot<count_requests):
        if (currentTime + time_quant <= timeNew): # истёк очередной квант времени
           pass
        else: # прибыла новая заявка
            pass

    currentTime =  max(currentTime, lastReq)
    # добавляем точки на краю
    addPoint(statGot, currentTime, curGot, curGot)
    addPoint(statDone, currentTime, curDone, curDone)
    addPoint(statRefused, currentTime, curRefused, curRefused)
    addPoint(statQueue, currentTime, len(queue), len(queue))

    return {"statGot":statGot,
    "statDone":statDone,
    "statRefused":statRefused,
    "statQueue":statQueue,
    "statWorkflow":statWorkflow,
    "statGotTime":statGotTime}
