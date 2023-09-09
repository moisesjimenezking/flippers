def Code(status):
    listStatus = {
        "AVAILABLE"   : 2,
        "UNAVAILABLE" : 1,
    }
    
    return listStatus[status]

def CodeID(status):
    listStatus = {
        2 : "AVAILABLE",
        1 : "UNAVAILABLE",
    }
    
    return listStatus[status]