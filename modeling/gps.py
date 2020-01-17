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
        if self.channels_gps[req["channel"]] is None:  # текущий канал не обслуживается
            for request in self.channels_gps:
                if request != numNew and self.channels_gps[request]["end"] != 0:
                    el = self.channels_gps[request]
                    el["done"] += ((el["end"] - el["prevStart"]) / el["end"]) * (el["totalWork"] - el["done"])

            self._recalculateEndTime_()

        else:  # текущий канал обслуживается, ставим в очередь
            (self.queue[req["channel"]]).append(req)

    # пересчитать сроки окончания для gps
    def _recalculateEndTime_(self):
        sum_weight = 0
        for i in range(self.count_channels):
            if self.channels_gps[i] is not None:
                sum_weight += self.weights_dict[i]

        for i in range(self.count_channels):
            el = self.channels_gps[i]
            el["end"] = self.currentTime + (el["totalWork"] - el["done"]) * self.weights_dict[i] / sum_weight

    # получить имя заявки, которую закончат обслуживать следующей
    def getNext(self):
        minTime = None
        name = None
        for ch in self.channels_gps:
            if ch is not None and (minTime is None or ch["end"] < minTime):
                minTime = ch["end"]
                name = ch["name"]
        return name

    # обслужить следующую заявку
    def serve(self):
        minTime = None
        channel = None
        for ch in self.channels_gps:
            if self.channels_gps[ch] is not None and (minTime is None or self.channels_gps[ch]["end"] < minTime):
                minTime = self.channels_gps[ch]["end"]
                channel = ch

        if channel is not None:
            req = self.queue[channel][0]
            self.queue[channel].remove(req)
