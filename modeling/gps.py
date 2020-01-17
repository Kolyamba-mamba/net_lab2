class GPS_simulator:
    def __init__(self, count_channels, weights_dict):
        self.currentTime = 0
        self.count_channels = count_channels
        self.weights_dict = weights_dict

        # очередь
        self.queue = {key: [] for key in range(self.count_channels)}

        # обслуживаемые заявки
        # вид:
        # { 0: {"name":'t1', "got": 0, "start":0, "end": 7, "channel":, "totalWork":, "done": , "prevStart":},
        #   1: {"name":'t2', "got": 2, "start":2, "end": 11,"channel":, "totalWork":, "done": , "prevStart":} }
        # done — количество выполненной работы
        # totalWork — общее количество работы, нужное для выполнения заявки
        # prevStart — время прошлого пересчёта окончания работы
        self.channels_gps = {key: None for key in range(self.count_channels)}

    # добавляем заявку на обслуживание
    def addRequest(self, req):
        numNew = req["channel"]

        if self.channels_gps[numNew] is None:  # текущий канал не обслуживается
            for request in self.channels_gps:
                el = self.channels_gps[request]
                if request != numNew and el is not None and el["end"]!=0:
                    el["done"] += ((el["end"] - el["prevStart"]) / el["end"]) * (el["totalWork"] - el["done"])
                    el["prevStart"] = self.currentTime
            self._recalculateEndTime_()
            self.channels_gps[numNew] = req

        else:  # текущий канал обслуживается, ставим в очередь
            (self.queue[req["channel"]]).append(req)

    # пересчитать сроки окончания для gps
    def _recalculateEndTime_(self):
        sum_weight = 0
        for i in range(self.count_channels):
            if self.channels_gps[i] is not None:
                sum_weight += self.weights_dict[i]
        if sum_weight != 0: # если равно нулю, то заявок нет, пересчитывать не нужно
            for i in range(self.count_channels):
                if self.channels_gps[i] is not None:
                    el = self.channels_gps[i]
                    el["end"] = self.currentTime + (el["totalWork"] - el["done"]) * self.weights_dict[i] / sum_weight

    # получить имя заявки, которую закончат обслуживать следующей
    def getNext(self):
        minTime = None
        name = None
        for ch in self.channels_gps:
            if self.channels_gps[ch] is not None and (minTime is None or self.channels_gps[ch]["end"] < minTime):
                minTime = self.channels_gps[ch]["end"]
                name = self.channels_gps[ch]["name"]
        return name

    # обслужить заявку
    def serve(self):
        print("serve")
        print(self.channels_gps)
        minTime = None
        channel = None
        for ch in self.channels_gps:
            if self.channels_gps[ch] is not None and (minTime is None or self.channels_gps[ch]["end"] < minTime):
                minTime = self.channels_gps[ch]["end"]
                channel = ch

        if channel is None:
            return

        self.currentTime = minTime
        
        if len(self.queue[channel]) > 0:
            print("ы")
            req = self.queue[channel][0]
            self.queue[channel].remove(req)
            self.channels_gps[channel] = req
        else:
            self.channels_gps[channel] = None

        self._recalculateEndTime_()

