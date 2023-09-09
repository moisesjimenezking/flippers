from .classStructure import DeliveryClass
from modules.bots.classStructure import BootsClass
from modules.chatters.model import Chatters
from .statusCodes import Code
import logging

logging.basicConfig(level=logging.DEBUG)

class Delivery:
    
    @classmethod
    def getData(cls, data):
        try:
            if "status" in data:
                status = Code(data["status"])
                data.pop("status")
                data.update({"status_id": status})
                
            response = DeliveryClass.getData(**data)
            if(len(response) == 0):
                raise Exception("Sin datos.", 404)
            else:
                response = {"response":response, "status_http": 200}
        except Exception as e:
            response = {"response":{"message":str(e)}, "status_http": 404}
        
        return response

    @classmethod
    def postData(cls, data):
        try:
            updateDirection = dict()
            if "phone_chatters" in data and ("bot_id" in data or "bot_name" in data):
                if "bot_id" in data:    
                    bot = BootsClass.getDataSearchBot(**{"id":data["bot_id"]})
                    if "name" not in bot:
                        raise Exception("Bot no encontrado.")
                    
                    data.pop("bot_id")
                    data["bot_name"] = bot["name"]
                
                updateDirection.update({
                    "chatter_phone":data["phone_chatters"], 
                    "bot_name":data["bot_name"], 
                    "last_direction":data["direction"]}
                )
                
                data.pop("phone_chatters")
                data.pop("bot_name")
            
            response = DeliveryClass.postData(**data)
            if len(response) > 0:
                response = {
                    "response":response,
                    "status_http":201
                }
                Chatters.putData(updateDirection)
            else:
                raise Exception("Fallo al crear el registro del delivery.", 400)
        except Exception as e:
            response = {
                'response':{
                    'message'  : e.args[0] if len(e.args) > 0 else str(e)
                },
                'status_http':e.args[1] if len(e.args) > 1 else 404
            }
            
        return response
    
    
    @classmethod
    def putData(cls, data):
        try:
            delivery = DeliveryClass.getDataFirst(data["id"])
            change = False
            
            for key, value in data.items():
                if hasattr(delivery, key): 
                    attr = getattr(delivery, key)
                    if str(attr) != str(value):
                        change =True
                        setattr(delivery, key, value)
            
            if change == True:          
                response = DeliveryClass.putData(delivery)
                if "id" not in response:
                    raise Exception("Ocurrio un error al intentar altualizar el delivery", 412)
            else:
                raise Exception("Sin cambios.", 304)
            
            response = {
                "response": response,
                "status_http": 201
            }
        except Exception as e:
            response = {
                'response':{
                    'message'  : e.args[0] if len(e.args) > 0 else str(e)
                },
                
                'status_http':e.args[1] if len(e.args) > 1 else 404
            }
            
        return response