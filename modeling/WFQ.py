import numpy as np
from collections import deque
from modeling.helper import *

def WFQ(input_stream, count_channels, work_stream, queue_length, count_requests, discipline, **kwargs):
    currentTime = 0
    statGot = {'x':[0], 'y':[0]}
    statDone = {'x':[0], 'y':[0]}
    statRefused = {'x':[0], 'y':[0]}
    statQueue = {'x':[0], 'y':[0]}
    curGot = 0
    curDone = 0
    curRefused = 0

    timeNew = 0 # время, когда придёт новая заявка
    timeDone = None # время, когда будет обслужена следующая заявка
    nameDone = None # имя заявки, которую обслужат следующей

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
    #{  0: [{"name":'t1', "got": 0, "start":0, "end": 7}, {"name": 't3', "got": 5, "start": 7, "end":14}],
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

    currentTime_gps = 0
    # очередь в симуляции gps
    # вид:
    #   { 0: ["name":'t1', "got":0],["name":'t3', "got":3],
    #   1: ["name":'t2', "got":2],["name":'t4', "got":5] }
    queue_gps = {key: [] for key in range(count_channels)}

    # обслуживаемые заявки в симуляции gps
    # вид:
    # { 0: {"name":'t1', "got": 0, "start":0, "end": 7},
    #   1: {"name":'t2', "got": 2, "start":2, "end": 11} }
    channels_gps = {key: None for key in range(count_channels)}

    while (curGot<count_requests):
        if (timeNew<=timeDone):
            


        # находим первую ненулевую заявку в GPS
        not_empty = False
        min_end_time = {}
        for el in channels_gps:
            if el!= {}:
                not_empty = True
                min_end_time = el
                break

        if (not_empty):
            # находим наиболее быстро обслуженную заявку по GPS
        
