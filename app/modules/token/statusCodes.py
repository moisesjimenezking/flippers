def Code(status):
    listStatus = {
        "FAILED" : 1,
        "SUCCESS"   : 2,
    }
    
    return listStatus[status]

def CodeID(status):
    listStatus = {
        1 : "FAILED",
        2 : "SUCCESS",
    }
    
    return listStatus[status]