from .classStructure import ticketsClass
from .statusCodes import Code
from .categoryCodes import CategoryID, Category
from modules.bots.classStructure import BootsClass
from modules.chatters.model  import Chatters
from library.boto import boto
from library.VerifyToken import verifyToken

import logging, re, bcrypt, random

logging.basicConfig(level=logging.DEBUG)

# UserLogClass = classStructure.UserLogClass
class Tickets:
    @classmethod
    def getData(cls, data):
        try:
            user_logged = verifyToken()
            if user_logged["status_http"] == 200:
                data.update({"id":user_logged["response"]["user_id"]})
                
            response = ticketsClass.getData(**data)
            if(len(response) == 0):
                raise Exception("Sin datos",404)
            else:
                response = {
                    "response":response, 
                    "status_http": 200
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
    def postDataBot(cls, data):
        try:
            #* bot_name -> se extrae el user_id
            if "bot_name" in data:
                bot = BootsClass.getDataFirst(data["bot_name"])
                if bot is None:
                    raise Exception("Bot no encontrado",404)
            else:
                raise Exception("No se ha enviado el bot",404)

            #* category -> se extrae el category
            category = Category(data["category"]) if "category" in data else 3

            #* chatter_phone -> se extrae el chatter_id
            Chatters.getVerifiData({"user_id":bot.user_id, "phone":data["chatter_phone"]})
            chatter = Chatters.getDataInternal({"user_id":bot.user_id, "phone":data["chatter_phone"]})
            if chatter["status_http"] == 200:
                chatter = chatter["response"][0]
            else:
                raise Exception("No se ha encontrado el chatter")
            
            #* message -> se define el mensaje y se pasa el chatter a lista de espera
            Chatters.putDataList({"id":chatter["id"], "status":"WAITING"})
            
            dataPost = {
                "category_id" : category,
                "user_id" : bot.user_id,
                "chatter_id" : chatter["id"],
                "message" : "¡Gracias por su interés! Un asesor se pondrá en contacto con usted pronto."
            }
            response = ticketsClass.postData(**dataPost)
            if "id" in response:
                response = {
                    "response"    : {
                        "message" : response["message"], 
                        "details" : list(), 
                        "error"   : None,
                        "note"    : None
                    },
                    "status_http" : 201
                }
            else:
                raise Exception("Ticket no creado")
        except Exception as e:
            response = {
                'response':{
                    "note": None,
                    'message': None,
                    'error' : e.args[0] if len(e.args) > 0 else str(e),
                    'details' : list()
                },
                
                'status_http':e.args[1] if len(e.args) > 1 else 404
            }
            
        return response