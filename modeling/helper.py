import numpy as np

def random(scale):
    return np.random.exponential(1/scale)

def addPoint(dict, time, oldvalue, value):
    dict["x"].append(time)
    dict["y"].append(oldvalue)
    if (oldvalue!=value):
        dict["x"].append(time)
        dict["y"].append(value)