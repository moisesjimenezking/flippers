from .classStructure import CommandsClass
from modules.bots.model import Bots
from library.boto import boto
from modules.bots.classStructure import BootsClass
from . import defaultCommands
from library.VerifyToken import verifyToken
import json, requests, re
import random
import logging
from . statusCodes import Code
logging.basicConfig(level=logging.DEBUG)

class Commands:
    
    @classmethod
    def getCommands(cls, data):
        try:
            message = ""
            details = list()
            default = defaultCommands.listDefaultCommands()
            
            #* consulta del bot
            consultbot = {"name":data["bot_name"]}
            bot = Bots.getBootsData(consultbot)
            if bot["status_http"] != 200:
                raise Exception("Bot no encontrado")
            
            bot = bot["response"][0]
                   
            Commands = CommandsClass.getData(**{"code":data["code"],"bot_id":bot["id"]})

            if(len(Commands) > 0):
                if type(Commands[0]["message"]) == list:
                    message = random.choice(Commands[0]["message"])
                else:
                    message = Commands[0]["message"]

                details.append({"message":message,"url":Commands[0]["file"]})
                
            if len(message) > 0:
                response = {
                    "response":{
                        "message": None,#message.replace("\"", ""),
                        "details": details,
                        "note": None,
                        "error": None
                    },
                    "status_http": 200
                }
            elif data["code"] in default:
                response = {
                    "response":{
                        "message": default[data["code"].lower()],
                        "details": list(),
                        "note": None,
                        "error": None
                    },
                    "status_http": 200
                }
            else:
                raise Exception("No encontrado", 404)
        except Exception as e:
            response = {
                'response':{
                    'message' : None,
                    'error'   : e.args[0] if len(e.args) > 0 else str(e),
                    'details' : list(),
                    "note"    : None
                },
                
                'status_http':e.args[1] if len(e.args) > 1 else 404
            }
            
        return response 
    
    @classmethod
    def postCommands(cls, data):
        try:
            user_logged = verifyToken()["response"]["user_id"]
            consultbot = {"user_id":user_logged}
            bot = Bots.getBootsData(consultbot)
            if bot["status_http"] != 200:
                raise Exception("Bot no encontrado")
            
            bot = bot["response"][0]
            data["bot_id"] = bot["id"]
            
            messages = list()
            for x in range(len(data["responses"].split(";response:"))):
                if len(data["responses"].split(";response:")[x]) > 0:
                    messages.append(data["responses"].split(";response:")[x])

            data.update({"message":messages, "code":data["intent"]})
            data["message"] = messages
            data.pop("responses")
            data.pop("intent")
            
            if "file" in data:
                if data["file"] is None or len(data["file"]) == 0:
                    data.pop("file")
                    data.update({"file":None})
                else:
                    product_name = re.sub(r"[^\w\s]", "", data["code"]).replace(" ", "_")+"."+data["file"].split("/")[1].split(";")[0]
                    base64 = data["file"].split(",")[-1]
                    content_type = data["file"].split(":")[1].split(";")[0]
                    url = boto(bot["name"], product_name, base64, content_type)
                    data.pop("file")
                    if url["status_http"] == 200:
                        data.update({"file":url["response"]["url"]})
                    else:
                        data.update({"file":None})

            response = CommandsClass.postData(**data)
            if len(response) > 0:
                response[0].update({"responses":response[0]["message"], "intent":response[0]["code"]})
                response[0].pop("message")
                response[0].pop("code")
                    
            response = {
                "response": "Fallo al crear el comando." if 'message' in response else response[0], 
                "status_http": 404 if 'message' in response else 201
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
    def putCommands(cls, data):
        try:    
            commands = CommandsClass.getDataFirst(data.get("id"))
            user_logged = verifyToken()["response"]["user_id"]
            bot = BootsClass.getDataFirstUser(user_logged)
            
            if "name" not in bot:
                raise Exception("Este usuario no posee bots")
            
            messages = list()
            if "responses" in data:
                logging.debug(str(data["responses"]))
                logging.debug(str(data.get("responses")))
                
                for x in range(len(data["responses"].split(";response:"))):
                    logging.debug(str(x))
                    logging.debug(str(data["responses"].split(";response:")[x]))
                    if len(data["responses"].split(";response:")[x]) > 0:
                        messages.append(data["responses"].split(";response:")[x])
                        
                data.update({"message":messages})
                data.pop("responses")
                
            if "intent" in data:
                data.update({"code":data["intent"]})
                data.pop("intent")
                
            if "status_id" in data:
                status_id = Code(data["status_id"])
                data.pop("status_id")
                data.update({"status_id":status_id})
            
            if "file" in data:
                if data["file"] is None or len(data["file"]) == 0:
                    data.pop("file")
                    data.update({"file":None})
                else:
                    product_name = re.sub(r"[^\w\s]", "", commands.code).replace(" ", "_")+"."+data["file"].split("/")[1].split(";")[0]
                    base64 = data["file"].split(",")[-1]
                    content_type = data["file"].split(":")[1].split(";")[0]
                    url = boto(bot["name"], product_name, base64, content_type)
                    data.pop("file")
                    data.update({"file":url["response"]["url"]})
                
            change = False
            
            for key, value in data.items():
                if hasattr(commands, key):
                    value = messages if key == "message" else value
                    
                    attr = getattr(commands, key)
                    if str(attr) != str(value):
                        change =True
                        setattr(commands, key, value)

            if(change):
                response = CommandsClass.putData(commands)
                if "id" in response :
                    response.update({"responses":response["message"], "intent":response["code"]})
                    response.pop("message")
                    response.pop("code")
                    
                response = {"response":response, "status_http": 404 if 'message' in response else 201}
            else:
                raise Exception("Sin cambios", 304)

        except Exception as e:
            response = {
                'response':{
                    'message': e.args[0] if len(e.args) > 0 else str(e)
                },
                
                'status_http':e.args[1] if len(e.args) > 1 else 400
            }
            
        return response
    
    @classmethod
    def getCommandsApp(cls, data):
        try:
            user_logged = verifyToken()["response"]["user_id"]
            bot = BootsClass.getDataFirstUser(user_logged)
            if "name" not in bot:
                raise Exception("Este usuario no posee bots")
            
            listCommands = CommandsClass.getData(**{"bot_id":bot["id"]})
            comands = list()

            for y in range(len(listCommands)):
                if "id" in listCommands[y]:
                    comands.append(
                        {
                            "id"              : listCommands[y]["id"],
                            "bot_id"          : listCommands[y]["bot_id"],
                            "intent"          : listCommands[y]["code"], 
                            "responses"       : listCommands[y]["message"] if isinstance(listCommands[y]["message"], list) else [listCommands[y]["message"]],
                            "default"         : False,
                            "file"            : listCommands[y]["file"],
                            "status_id"       : listCommands[y]["status_id"],
                            "datetime"        : listCommands[y]["datetime"],
                            # "datetime_update" : listCommands[y]["datetime_update"]
                        }
                    )
                    
            if len(comands) > 0:
                response = {
                    "response":comands,
                    "status_http": 200
                }
            else:
                raise Exception("Sin comandos.", 404)
        except Exception as e:
            response = {
                'response':{
                    'message': 'Se produjo un error',
                    'error'  : e.args[0] if len(e.args) > 0 else str(e)
                },
                
                'status_http':e.args[1] if len(e.args) > 1 else 404
            }
            
        return response 
    
    
    @classmethod
    def deleteCommand(cls, data):
        try:
            user = CommandsClass.getDataFirst(data["id"])
            if user is not None: 
                response = CommandsClass.deletData(user)
                if "message" in response:
                    response = {
                        "response"    : response, 
                        "status_http" : 200
                    }
                else:
                    raise Exception("Ocurrio un error al eliminar el comando.", 500)
            else:
               raise Exception("comando no encontrado.", 404)
        except Exception as e:
            response = {
                'response':{
                    'message'  : e.args[0] if len(e.args) > 0 else str(e)
                },
                
                'status_http':e.args[1] if len(e.args) > 1 else 404
            }
            
        return response