def Code(status):
    listStatus = {
        "CANCELLED": 1,
        "SOLD"     : 2,
        "PENDING"  : 3
    }
    
    return listStatus[status]

def CodeID(status):
    listStatus = {
        1 : "CANCELLED",
        2 : "SOLD",
        3 : "PENDING"
    }
    
    return listStatus[status]