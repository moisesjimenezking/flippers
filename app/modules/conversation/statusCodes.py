def Code(status):
    listStatus = {
        "WAITING"   : 1,
        "ATTENDING" : 2,
        "CLOSE"     : 3,
    }
    
    return listStatus[status]

def CodeID(status):
    listStatus = {
        1 : "WAITING",
        2 : "ATTENDING",
        3 : "CLOSE",
    }
    
    return listStatus[status]