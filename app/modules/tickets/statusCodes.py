def Code(status):
    listStatus = {
        "AVAILABLE"   : 1,
        "UNAVAILABLE" : 2,
    }
    
    return listStatus[status]

def CodeID(status):
    listStatus = {
        1 : "AVAILABLE",
        2 : "UNAVAILABLE",
    }
    
    return listStatus[status]