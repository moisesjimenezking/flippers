def Category(status):
    listStatus = {
        "CLAIM" : 1,
        "SHOP"  : 2,
        "OTHER" : 3,
    }
    
    category = listStatus[status] if status in listStatus else 3
    return category

def CategoryID(status):
    listStatus = {
        1 : "CLAIM",
        2 : "SHOP",
        3 : "OTHER",
    }
    
    return listStatus[status]