from modeling.RR import RR
from modeling.simpleSMO import simpleSMO


discipline = {
    "FIFO", 
    "LIFO",
    "RR"
}

def modeling(discipline, kwargs):
    res = None
    print(discipline)

    if discipline == "RR":
        res = RR(**kwargs)
    elif discipline in ["FIFO", "LIFO", "RAND"]:
        res = simpleSMO(**kwargs)
    else:
        ValueError("not found discipline")
    
    return res