from .classStructure import ChattersClass
from datetime import datetime, timedelta
from modules.bots.classStructure import BootsClass
from modules.conversation.classStructure import ConversationClass
from modules.sales.classStructure import SalesClass
from modules.commands.classStructure import CommandsClass 
from modules.conversation.statusCodes import Code as ConversationStatus
from modules.commands import defaultCommands
from modules.product.classStructure import ProductClass
import logging
from library.VerifyToken import verifyToken

logging.basicConfig(level=logging.DEBUG)

class Chatters:
    
    @classmethod
    def getData(cls, data):
        try:
            user_logged = verifyToken()["response"]["user_id"]
            data.update({"user_id":user_logged})
            response = ChattersClass.getDataApp(**data)
            if(len(response) == 0):
                response = {"response":{"message": "Sin datos"}, "status_http": 404}
            else:
                response = {"response":response, "status_http": 200}
        except Exception as e:
            response = {"response":{"message":str(e)}, "status_http": 404}
        
        return response
    
    @classmethod
    def getListBlack(cls, data):
        try:
            user_logged = verifyToken()["response"]["user_id"]
            data.update({"user_id":user_logged})
            response = ChattersClass.getDataApp(**{"list_black":1})
            if(len(response) == 0):
                raise Exception("Sin datos", 404)
            else:
                response = {
                    "response":response, 
                    "status_http": 200
                }
        except Exception as e:
            response = {
                'response':{
                    'error': 'Se produjo un error',
                    'message'  : e.args[0] if len(e.args) > 0 else str(e)
                },
                
                'status_http':e.args[1] if len(e.args) > 1 else 404
            }
        return response
    
    @classmethod
    def getDataInternal(cls, data):
        try:
            if 'datetime' in data:
                datetimeSearch = datetime.now().strftime('%Y-%m-%d')+' 00:00:00'
                response = ChattersClass.getDataTime(datetimeSearch, data["user_id"])
            else:
                response = ChattersClass.getData(**data)
            
            if(len(response) == 0):
                response = {"response":{"message": "Sin datos"}, "status_http": 404}
            else:
                response = {"response":response, "status_http": 200}
        except Exception as e:
            response = {"response":{"message":str(e)}, "status_http": 404}
        
        return response
    
    @classmethod
    def getVerifiData(cls, data):
        try:
            response = cls.postData({"user_id":data["user_id"], "phone":data["chatter_phone"]})
            
            if(len(response) == 0):
                response = {"response":{"message": "Sin datos"}, "status_http": 404}
            else:
                response = {"response":response, "status_http": 200}
        except Exception as e:
            response = {"response":{"message":str(e)}, "status_http": 404}
        
        return response


    @classmethod
    def postData(cls, data):
        try:
            response = ChattersClass.postData(**data)
            response = {
                "response": response["message"] if 'message' in response else response, 
                "status_http": 404 if 'message' in response else 201
            }
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
    def putData(cls, data):
        try:  
            if "status" in data:
                conversation = ConversationClass.getDataFirstPut(data["id"])
                list = {
                    "WAITING"   : 'list_wait', 
                    "ATTENDING" : 'list_attention',
                    "LOCKED"    : 'list_black'
                }
                
                for key, value in list.items():
                    if key == data["status"]:
                        data.update({value : 1})
                    else:
                        if data["status"] == "CLOSE":
                            if value != "list_black":
                                data.update({value : 0})
                        else:
                            data.update({value : 0})
                                  
                if (data["status"] in list and data["status"] != "LOCKED") or data["status"] == "CLOSE":
                    setattr(conversation, "status_id", ConversationStatus(data["status"]))
                    ConversationClass.putData(conversation)
                    
            if "id" not in data:
                bot = BootsClass.getDataFirst(data["bot_name"])
                if bot is None:
                    raise Exception("Bot no encontrado.")
                
                data.pop("bot_name")
                
                user = ChattersClass.getDataFirst(bot.user_id,data["chatter_phone"])
            else:
                if "status" in data:
                    data.pop("id")
                    user = ChattersClass.getDataFirstIdPut(conversation.chatter_id)
                else:
                    user = ChattersClass.getDataFirstIdPut(data["id"])

            change = False
            
            for key, value in data.items():
                if hasattr(user, key): 
                    attr = getattr(user, key)
                    if str(attr) != str(value):
                        change =True
                        setattr(user, key, value)

            if(change):
                response = ChattersClass.putData(user)
                if "id" in response:
                    user_id = response["user_id"]
                    response = {
                        "response":response, 
                        "status_http": 201
                    }
                    
                    ChattersClass.satisfactionData(user_id)  
                else:
                    raise Exception("Se ha producido un error en la actualización de los datos, por favor, espere unos minutos y vuelva a intentar.", 304)
            else:
                raise Exception("Se ha producido un error en la actualización de los datos, por favor, espere unos minutos y vuelva a intentar.", 304)

        except Exception as e:
            response = {
                'response':{
                    'error': 'Se produjo un error',
                    'message'  : e.args[0] if len(e.args) > 0 else str(e)
                },
                
                'status_http':e.args[1] if len(e.args) > 1 else 404
            }
            
        return response
    
    @classmethod
    def getDataList(cls, data):
        try:
            updateChatter = dict()
            search = dict()
            
            search.update({"phone":data["chatter_phone"]})

            bot = BootsClass.getDataFirst(data["bot_name"])
            if bot is None:
                raise Exception("bot no encontrado")
            else:
                search.update({"user_id":bot.user_id})

            #* ADD datetime_update
            updateChatter.update({"datetime_update":datetime.now().strftime('%Y-%m-%d %H:%M:%S')})

              
            if "chatter_name" in data:
                updateChatter.update({"name":data["chatter_name"]})
                
            if "profile_img" in data:
                updateChatter.update({"profile_img":data["profile_img"]})
                
                
            cls.getVerifiData({"user_id":bot.user_id, "chatter_phone":data["chatter_phone"]})
            response = ChattersClass.getData(**search)
            
            user = ChattersClass.getDataFirst(bot.user_id,search["phone"])
            change = False
            
            for key, value in updateChatter.items():
                if hasattr(user, key): 
                    attr = getattr(user, key)
                    if str(attr) != str(value):
                        change =True
                        setattr(user, key, value)
            if(change):
                ChattersClass.putData(user)
            
            if(len(response) == 0):
                response = {"response":{"message": "Sin datos"}, "status_http": 400}
            else:
                #* Si el chatter se registro en los ultimos 7 dias se define como nuevo cliente
                isNewClient = (datetime.now() - response[0]["datetime"]) < timedelta(days=7)
                
                #* Si el chatter tiene mas de 3 compras en los ultimos 30 dias se considera un chatter fiel
                sales = SalesClass.getDataFidelity(data["chatter_phone"])
                isFidelity = True if len(sales) >= 3 else False
                
                #* Comandos del bot
                commands = [c.lower() for c in list(defaultCommands.listDefaultCommands()) + list(CommandsClass.botCommands(bot.id))]

                #* productos del bot
                products = ProductClass.getData(**{"bot_id": bot.id, "user_id": bot.user_id})
                listProducts = []
                for element in products:
                    if len(listProducts) < 3:
                        listProducts.append(element["name"])
                    else:
                        break
                    
                response = {
                    "list_black"                : bool(response[0]["list_black"]),
                    "list_wait"                 : bool(response[0]["list_wait"]),
                    "list_attention"            : bool(response[0]["list_attention"]),
                    "hasDelivery"               : True,
                    "isNewClient"               : isNewClient,
                    "isFidelity"                : isFidelity,
                    "commands"                  : list(dict.fromkeys(commands)),
                    "lastIteration"             : (response[0]["datetime_update"] - timedelta(hours=4)).strftime('%Y-%m-%d %H:%M:%S'),
                    "listTopProducts"           : listProducts,
                    "can_read_audio_message"    : False,
                    "can_create_appointment"    : False
                }
                
                response = {"response":response, "status_http": 200}
        except Exception as e:
            response = {"response":{"message":str(e)}, "status_http": 400}
        
        return response
    
    @classmethod
    def putDataList(cls, data):
        try:
            list = {
                "WAITING"   : 'list_wait', 
                "ATTENDING" : 'list_attention',
                "LOCKED"    : 'list_black'
            }
            
            update = dict()
            for key, value in list.items():
                if data["status"] == key:
                    update.update({value:1})
                else:
                    update.update({value:0})
            
            chatters = ChattersClass.getDataFirstIdPut(data["id"])
            change = False
                
            for key, value in update.items():
                if hasattr(chatters, key): 
                    attr = getattr(chatters, key)
                    if str(attr) != str(value):
                        change =True
                        setattr(chatters, key, value)
                        
            if(change):
                response = ChattersClass.putData(chatters)
                if "id" in response:
                    response = {
                        "response":response, 
                        "status_http": 201
                    }
                else:
                    raise Exception("no modifid")
            else:
                raise Exception("no modifid")
            
        except Exception as e:
            response = {
                "response":{
                    "message":str(e)
                }, 
                "status_http": 400}
        
        return response