def Code(status):
    listStatus = {
        "UNAVAILABLE" : 1,
        "AVAILABLE"   : 2,
    }
    
    return listStatus[status]

def CodeID(status):
    listStatus = {
        1 : "UNAVAILABLE",
        2 : "AVAILABLE",
    }
    
    return listStatus[status]