from modeling.RR import RR
from modeling.simpleSMO import simpleSMO
from modeling.SJN import SJN


discipline = {
    "FIFO", 
    "LIFO",
    "RR"
}

def modeling(discipline, kwargs):
    res = None

    if discipline == "RR":
        res = RR(**kwargs)
    elif discipline in ["FIFO", "LIFO", "RAND"]:
        res = simpleSMO(**kwargs)
    elif discipline == "SJN":
        res = SJN(**kwargs)
    else:
        ValueError("not found discipline")
    
    return res