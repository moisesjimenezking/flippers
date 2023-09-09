from .classStructure import ClaimsClass
from modules.bots.classStructure import BootsClass
from datetime import datetime, timedelta
class Claims:
    
    @classmethod
    def getData(cls, data):
        try:
            response = ClaimsClass.getData(**data)
            if(len(response) == 0):
                raise Exception("Sin datos.")
            
            response = {
                "response"      : response,
                "status_http"   : 200  
            }
        except Exception as e:
            response = {
                'response':{
                    'message'  : e.args[0] if len(e.args) > 0 else str(e)
                },
                
                'status_http':e.args[1] if len(e.args) > 1 else 404
            }
            
        return response 
    
    @classmethod
    def postData(cls, data):
        try:
            if "bot_name" in data:
                bot = BootsClass.getDataFirst(data["bot_name"])
                if bot.id is not None:
                    data.pop("bot_name")
                    data.update({"bot_id":bot.id})
                else:
                    raise Exception("Bot no encontrado", 400)
                
            response = ClaimsClass.postData(**data)
            if(len(response) == 0):
                raise Exception("Ocurrio un error al crear el reclamo", 400)
            
            response = {
                "response"      : response,
                "status_http"   : 201
            }
        except Exception as e:
            response = {
                'response':{
                    'message'  : e.args[0] if len(e.args) > 0 else str(e)
                },
                
                'status_http':e.args[1] if len(e.args) > 1 else 404
            }
            
        return response
    
    @classmethod
    def getDataTime(cls, data):
        try:
            if data["type"].upper() == "CURRENT":
                datetimeStart = datetime.now().strftime('%Y-%m-%d')+' 00:00:00'
                datetimeEnd = datetime.now().strftime('%Y-%m-%d')+' 23:59:59'
            elif data["type"].upper() == "OLD":
                datetimeStart = (datetime.now() - timedelta(days=1)).strftime('%Y-%m-%d')+' 00:00:00'
                datetimeEnd = (datetime.now() - timedelta(days=1)).strftime('%Y-%m-%d')+' 23:59:59'
                  
            response = ClaimsClass.getDataTime(data["bot_id"], datetimeStart, datetimeEnd)
            if(len(response) == 0):
                raise Exception("Sin datos.")
            
            response = {
                "response"      : response,
                "status_http"   : 200  
            }
        except Exception as e:
            response = {
                'response':{
                    'message'  : e.args[0] if len(e.args) > 0 else str(e)
                },
                
                'status_http':e.args[1] if len(e.args) > 1 else 404
            }
            
        return response 