from modeling.RR import RR
from modeling.simpleSMO import simpleSMO
from modeling.SJN import SJN
from modeling.W2FQ import W2FQ
from modeling.WFQ import WFQ
from modeling.W2FQplus import W2FQplus
from modeling.DRR import DRR
from modeling.CSWFQ import CSWFQ


discipline = {
    "FIFO", 
    "LIFO",
    "RR",
    "WFQ",
    "W2FQ",
    "W2FQ+",
    "DRR",
    "CS-WFQ",
    "SFBA"
}

def modeling(discipline, kwargs):
    res = None

    if discipline == "RR":
        res = RR(**kwargs)
    elif discipline in ["FIFO", "LIFO", "RAND"]:
        res = simpleSMO(**kwargs)
    elif discipline == "SJN":
        res = SJN(**kwargs)
    elif discipline == "WFQ":
        res = WFQ(**kwargs)
    elif discipline == "W2FQ":
        res = W2FQ(**kwargs)
    elif discipline == "W2FQ+":
        res = W2FQplus(**kwargs)
    elif discipline == "DRR":
        res = DRR(**kwargs)
    elif discipline == "CS-WFQ":
        res = CSWFQ(**kwargs)
    else:
        ValueError("not found discipline")
    
    return res