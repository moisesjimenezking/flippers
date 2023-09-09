def Code(status):
    listStatus = {
        "CANCELLED" : 1,
        "WAITING"   : 2,
        "SENT"      : 3,
        "DELIVERED" : 4 
    }
    
    return listStatus[status]

def CodeID(status):
    listStatus = {
        1 : "CANCELLED",
        2 : "WAITING",
        3 : "SENT",
        4 : "DELIVERED" 
    }
    
    return listStatus[status]