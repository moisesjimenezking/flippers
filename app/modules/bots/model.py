from . import classStructure
from flask import jsonify, request, json
from modules.chatters.model import Chatters
from modules.claims.model import Claims
from modules.sales.classStructure import SalesClass
from modules.subscriptions.model import Subscriptions
from datetime import datetime, timedelta
import logging, re
from library.boto import boto
from library.VerifyToken import verifyToken
from .statusCodes import Code

logging.basicConfig(level=logging.DEBUG)

BootsClass = classStructure.BootsClass

class Bots:
    
    @classmethod
    def getBootsData(cls, data):
        try:
            response = BootsClass.getData(**data)
            if(len(response) == 0):
                response = {"response":{"message": "Sin datos"}, "status_http": 400}
            else:
                response = {"response":response, "status_http": 200}
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
    def postData(cls, data):
        try:
            if "user_id" not in data:
                user_logged = verifyToken()
                if user_logged["status_http"] != 200:
                    raise Exception(user_logged["response"]["message"])
                
                data["user_id"] = user_logged["response"]["user_id"]
                
            if "qr" in data:
                qr_name = re.sub(r"[^\w\s]", "", data["name"]).replace(" ", "_")+"."+data["qr"].split("/")[1].split(";")[0]
                base64 = data["qr"].split(",")[-1]
                content_type = data["qr"].split(":")[1].split(";")[0]
                url = boto(data["name"], qr_name, base64, content_type)

                if url["status_http"] == 200:
                    data["qr"] = url["response"]["url"]
                else:
                    raise Exception("error url", 500)
                
            if "plan_id" in data:
                plan = data["plan_id"]
                
            #* Data Post
            data = {
                "objetive"        : data["corpus"]["objetive"] if "objetive" in data["corpus"] else None,
                "social_links"    : data["corpus"]["social_links"] if "social_links" in data["corpus"] else None,
                "summary"         : data["corpus"]["summary"] if "sumamary" in data["corpus"] else None,
                "user_id"         : data["user_id"],
                "phone"           : data["phone"],
                "name"            : data["name"],
                "has_delivery"    : 1 if "has_delivery" in data["corpus"] else 0,
                "has_descounts"   : 1 if "has_descounts" in data["corpus"] else 0,
                "has_promotions"  : 1 if "has_promotions" in data["corpus"] else 0,
                "web_page"        : data["corpus"]["web_page"] if "web_page" in data["corpus"] else None,
                "bussiness_hours" : data["corpus"]["bussiness_hours"] if "bussiness_hours" in data["corpus"] else None,
            }

            updateBot = False
            verificBot = BootsClass.getData(**{"user_id":data["user_id"]})
            if len(verificBot) > 0:
                updateBot = True
                
            if updateBot:
                bot = BootsClass.getDataFirst(verificBot[0]["name"])
                change = False
                
                for key, value in data.items():
                    if hasattr(bot, key): 
                        attr = getattr(bot, key)
                        if str(attr) != str(value):
                            change =True
                            setattr(bot, key, value)

                if(change):
                    response = BootsClass.putData(bot)
                    response = {
                        "response":response, 
                        "status_http": 201
                    }
                else:
                    raise Exception("Bot no actualizado")
            else:
                response = BootsClass.postData(**data)
                if 'message' in response:
                    raise Exception(response['message'], 412)
                
                response.update({"message":"ok"})
                response = {
                    "response":response, 
                    "status_http": 201
                }
                
            if response["status_http"] == 201:
                plan = 1 if "plan_id" not in locals() else plan
                create = Subscriptions.postSubscriptionsData({"plan_id":plan})
                logging.debug(str(create))
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
            if 'id' in data:
                boots = BootsClass.getDataFirst(data.get("id"))
                data.pop("id")
                
            if 'bot_name' in data:
                boots = BootsClass.getDataFirst(data.get("bot_name"))
                data.pop("bot_name")
                
            if 'status' in data:
                data["status_id"] = Code(data["status"])
                data.pop("status")
                
            if "qr" in data:
                qr_name = re.sub(r"[^\w\s]", "", boots.name).replace(" ", "_")+"."+data["qr"].split("/")[1].split(";")[0]
                base64 = data["qr"].split(",")[-1]
                content_type = data["qr"].split(":")[1].split(";")[0]
                url = boto(boots.name, qr_name, base64, content_type)

                if url["status_http"] == 200:
                    data["qr"] = url["response"]["url"]
                else:
                    raise Exception("error url", 500)
                
            change = False
            
            for key, value in data.items():
                if hasattr(boots, key): 
                    attr = getattr(boots, key)
                    if str(attr) != str(value):
                        change =True
                        setattr(boots, key, value)

            if(change):
                response = BootsClass.putData(boots)
                response = {"response":response, "status_http": 404 if 'message' in response else 201}
            else:
                if "chatters_active" in data:
                    raise Exception("Sin cambios.", 200)
                else:
                    raise Exception("Sin cambios.", 304)

        except Exception as e:
            response = {
                'response':{
                    'message'  : e.args[0] if len(e.args) > 0 else str(e)
                },
                
                'status_http':e.args[1] if len(e.args) > 1 else 404
            }
            
        return response
    
    
    @classmethod
    def getStatistic(cls, data):
        try:
            
            bot = BootsClass.getData(**{"user_id":data["user_id"]})
            if len(bot) == 0:
                raise Exception("Este usuario no posee bots")
            
            #* Se extrae la cantidad de clientes
            chatters = Chatters.getDataInternal({"user_id":data["user_id"]})
            if chatters["status_http"] != 200:
                chattersQuantity = 0
                chattersPercentage = "0%"
            else:
                chattersQuantity = len(chatters["response"])
                chatters = Chatters.getDataInternal({"user_id":data["user_id"], "datetime":True})
                if chatters["status_http"] == 200:
                    if len(chatters["response"]) == chattersQuantity or chattersQuantity == 0:
                        chattersPercentage = "0%"
                    else:
                        chattersPercentage = str(round(((chattersQuantity - len(chatters["response"]))/len(chatters["response"]))*100, 2))+"%"
                else:
                    chattersPercentage = "0%"
                                
            #* Se extrae la cantidad de reclamos de hoy
            claims = Claims.getDataTime({"bot_id":bot[0]["id"], "type":"current"})
            if claims["status_http"] != 200:
                claimsQuantity = 0
                claimsPercentage = "0%"
            else:
                claimsQuantity = len(claims["response"])
                
                claims = Claims.getDataTime({"bot_id":bot[0]["id"], "type":"old"})
                if claims["status_http"] == 200:
                    if len(claims["response"]) == claimsQuantity or claimsQuantity == 0:
                        claimsPercentage = "0%"
                    else:
                        claimsPercentage = str(round(((claimsQuantity - len(claims["response"]))/len(claims["response"]))*100, 2))+"%"
                else:
                    claimsPercentage = "100%"
                    
            #* Se extraen las ventas de hoy
            datetimeStart = datetime.now().strftime('%Y-%m-%d')+' 00:00:00'
            datetimeEnd = datetime.now().strftime('%Y-%m-%d')+' 23:59:59'
            sales = SalesClass.getDataTime(data["user_id"], datetimeEnd, datetimeStart)
            if len(sales) == 0:
                salesQuantity = 0
                salesPercentage = "0%"
            else:
                salesQuantity = len(sales)
                datetimeStart = (datetime.now() - timedelta(days=1)).strftime('%Y-%m-%d')+' 00:00:00'
                datetimeEnd = (datetime.now() - timedelta(days=1)).strftime('%Y-%m-%d')+' 23:59:59'
                sales = SalesClass.getDataTime(data["user_id"], datetimeEnd, datetimeStart)
                if len(sales) > 0:
                    if len(sales) == salesQuantity or salesQuantity == 0:
                        salesPercentage = "0%"
                    else:
                        salesPercentage = str(round(((salesQuantity - len(sales))/len(sales))*100, 2))+"%"
                else:
                    salesPercentage = "0%"
                    
            response = {
                "response":{
                    "chattersQuantity"  : chattersQuantity,
                    "chattersPercentage": chattersPercentage,
                    "claimsQuantity"    : claimsQuantity,
                    "claimsPercentage"  : claimsPercentage,
                    "salesQuantity"    : salesQuantity,
                    "salesPercentage"  : salesPercentage
                },
                "status_http":200
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