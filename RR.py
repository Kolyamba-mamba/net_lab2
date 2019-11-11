import numpy as np
from collections import deque

def getNextRequest(queue:deque):
    if len(queue)>0:
        return queue.popleft()
    else:
        return None

def random(scale):
    return np.random.exponential(1/scale)

def addPoint(dict, time, oldvalue, value):
    dict["x"].append(time)
    dict["y"].append(oldvalue)
    if (oldvalue!=value):
        dict["x"].append(time)
        dict["y"].append(value)

def RR(dataFromUI):
    input_stream = dataFromUI["input_stream"]
    count_channels = dataFromUI["count_channels"]
    work_stream = dataFromUI["work_stream"]
    queue_length = dataFromUI["queue_length"]
    count_requests = dataFromUI["count_requests"]
    discipline = dataFromUI["discipline"]
    time_quant = dataFromUI["time_quant"]
    buffer_size = dataFromUI["buffer_size"]
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
            queueChanged = False
            prevLen = len(queue)
            for ch in channels:
                if (channels[ch] != None):
                    if (channels[ch]["left"]<=time_quant):
                        curDone+=1
                        addPoint(statDone, currentTime+channels[ch]["left"], curDone-1 ,curDone)
                    else:
                        channels[ch]["left"]-=time_quant
                        buffer.append(channels[ch])
            currentTime += time_quant
            for ch in channels:
                if (len(buffer)!=0):
                    channels[ch] = getNextRequest(buffer)
                    channels[ch]["start"] = currentTime
                    channels[ch]["end"] = currentTime+min(time_quant, channels[ch]["left"])
                    statWorkflow[ch].append({"start":channels[ch]["start"],"end":channels[ch]["end"],"name":channels[ch]["name"]})
                elif (len(queue)!=0):
                    queueChanged = True
                    channels[ch] = getNextRequest(queue)
                    channels[ch]["start"] = currentTime
                    channels[ch]["end"] = currentTime+min(time_quant, channels[ch]["left"])
                    statWorkflow[ch].append({"start":channels[ch]["start"],"end":channels[ch]["end"],"name":channels[ch]["name"]})
                else:
                    channels[ch] = None

            if (len(queue)!=0 and len(buffer)<buffer_size):  
                queueChanged = True
                while (len(queue)!=0 and len(buffer)<buffer_size):
                    buffer.append(getNextRequest(queue))
            
            if (queueChanged):
                addPoint(statQueue, currentTime, prevLen, len(queue))
            
        else: # прибыла новая заявка
            lastReq = timeNew
            curGot+=1
            addPoint(statGot, timeNew, curGot-1, curGot)
            statGotTime.append({"name":'t'+str(curGot), "got":timeNew})         
            if (len(buffer)<buffer_size):
                buffer.append({"name":'t'+str(curGot), "got": timeNew, "left":random(work_stream)})
            elif (len(queue)<queue_length):
                queue.append({"name":'t'+str(curGot), "got": timeNew, "left":random(work_stream)})
                addPoint(statQueue, timeNew, len(queue)-1, len(queue))
            else:
                curRefused += 1
                addPoint(statRefused, timeNew, curRefused-1, curRefused)
            timeNew += random(input_stream)
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