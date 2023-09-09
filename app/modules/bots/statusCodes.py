def Code(status):
    listStatus = {
        "INACTIVE": 1,
        "ACTIVE"   : 2
    }
    
    return listStatus[status]

def CodeID(status):
    listStatus = {
        1:"INACTIVE",
        2:"ACTIVE"
    }
    
    return listStatus[status]