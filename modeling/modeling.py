from modeling.RR import RR
from modeling.simpleSMO import simpleSMO
from modeling.SJN import SJN
from modeling.W2FQ import W2FQ
from modeling.WFQ import WFQ
from modeling.W2FQplus import W2FQplus
from modeling.DRR import DRR
from modeling.CSWFQ import CSWFQ
from modeling.W2F2Q import WirelessWFQWorstCase


discipline = [
    "FIFO", 
    "LIFO",
    "RR",
    "WFQ",
    "W2FQ",
    "W2FQ+",
    "DRR",
    "CS-WFQ",
    "SFBA",
    "Wireless Worst-case Fair Weighted Fair Queueing (W2F2Q)",
    "Server Based Fairness Approach (SBFA)",
    "Channel State Independent Wireless Fair Queueing (CS-WFQ)",
    "Wireless Multiclass Priority Fair Queuing (MPFQ)"
]

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
    elif discipline == "Channel State Independent Wireless Fair Queueing (CS-WFQ)":
        res = CSWFQ(**kwargs)
    elif discipline == "Wireless Worst-case Fair Weighted Fair Queueing (W2F2Q)":
        res = WirelessWFQWorstCase(**kwargs)
    else:
        ValueError("not found discipline")
    
    return res