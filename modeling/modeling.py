from modeling.RR import RR
from modeling.simpleSMO import simpleSMO
from modeling.SJN import SJN
from modeling.W2FQ import W2FQ
from modeling.DRR import DRR

discipline = {
    "FIFO", 
    "LIFO",
    "RR",
    "W2FQ",
    "DRR"
}

def modeling(discipline, kwargs):
    res = None

    if discipline == "RR":
        res = RR(**kwargs)
    elif discipline in ["FIFO", "LIFO", "RAND"]:
        res = simpleSMO(**kwargs)
    elif discipline == "SJN":
        res = SJN(**kwargs)
    elif discipline == "W2FQ":
        res = W2FQ(**kwargs)
    elif discipline == "DRR":
        res = DRR(**kwargs)
    else:
        ValueError("not found discipline")
    
    return res