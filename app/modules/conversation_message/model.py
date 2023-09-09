from .classStructure import ConversationMessageClass
from library.boto import boto
from library.setting.generateString import generated
from modules.bots.classStructure import BootsClass
from modules.chatters.classStructure import ChattersClass
from modules.conversation.classStructure import ConversationClass
from library.VerifyToken import verifyToken
from modules.conversation.statusCodes import Code as ConversationStatus
import logging, re
import random
import string

logging.basicConfig(level=logging.DEBUG)

class ConversationMessage:
    @classmethod
    def getConversationMessage(cls, data):
        try:
            response = ConversationMessageClass.getData(**data)
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
    def postConversationMessage(cls, data):
        try:
            bot = BootsClass.getDataSearchBot(**{"name":data["bot_name"]})
            if "id" not in bot:
                raise Exception("Bot no encontrado.", 404)
            
            
            chatter = ChattersClass.getChattersFirst(**{"phone":re.sub(r"[^0-9]", "", data["chatter_phone"]), "user_id":bot["user_id"]})
            if "id" not in chatter:
                raise Exception("chatter no encontrado.", 404)
            
            status = [ConversationStatus("WAITING"),ConversationStatus("ATTENDING")]
            
            if "archive" in data and data["archive"] is not None:
                qr_name = generated(10)+"."+data["archive"].split("/")[1].split(";")[0]
                base64 = data["archive"].split(",")[-1]
                content_type = data["archive"].split(":")[1].split(";")[0]
                url = boto(data["bot_name"], qr_name, base64, content_type)

                if url["status_http"] == 200:
                    data["archive"] = url["response"]["url"]
                else:
                    raise Exception("error url", 500)
                
            conversation = None
            structure = False
            is_exist_conversation = True
            searchConveration = ConversationClass.getSearchFirst(status, bot["id"], chatter["id"])
            if "id" not in searchConveration:
                crateConversation = ConversationClass.postData(**{
                    "bot_id"     : bot["id"],
                    "chatter_id" : chatter["id"],
                })
                
                if "id" not in crateConversation:
                    raise Exception("No fue posible crear la conversacion.")
                else:
                    structure = True
                    is_exist_conversation = False
                    conversation = crateConversation["id"]
            else:
                status = searchConveration["status_id"]
                conversation = searchConveration["id"]
                
            if conversation is not None:
                createMessage = {
                    "conversation_id" : conversation,
                    "message"         : data["message"] if "message" in data and isinstance(data["message"], str) else None,
                    "archive_url"     : data["archive"] if "archive" in data else None
                }
                
                response = ConversationMessageClass.postData(**createMessage)
                
                if "id" in response:
                    result = ConversationClass.updateDatetime(conversation)
                    response = ConversationClass.getDataAll(**{"id":conversation})[0] if structure else response
                    response["status"] = response["status"] if structure else status
                    response["is_exist_conversation"] = is_exist_conversation
                    response = {
                        "response":response,
                        "status_http":201
                    }
                else:
                    raise Exception("No se agrego registro del mensaje")
            else:
                raise Exception("Conversacion no encontrada")
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
    def postConversationApp(cls, data):
        try:
            if "archive" in data:
                qr_name = generated(10)+"."+data["archive"].split("/")[1].split(";")[0]
                base64 = data["archive"].split(",")[-1]
                content_type = data["archive"].split(":")[1].split(";")[0]
                url = boto(generated(10), qr_name, base64, content_type)

                if url["status_http"] == 200:
                    data["archive"] = url["response"]["url"]
                else:
                    raise Exception("error url", 500)
                
            createMessage = {
                "conversation_id" : data["id"],
                "message"         : data["message"],
                "me"              : 1,
                "archive_url"     : data["archive"] if "archive" in data else None,
                "status"          : data["status"]
            }
            
            response = ConversationMessageClass.postData(**createMessage)
            if "id" in response:
                result = ConversationClass.updateDatetime(response["id"])
                response = {
                    "response":response,
                    "status_http":201
                }
            else:
                raise Exception("No se agrego registro del mensaje")

        except Exception as e:
            response = {
                'response':{
                    'message': 'Se produjo un error',
                    'error'  : e.args[0] if len(e.args) > 0 else str(e)
                },
                
                'status_http':e.args[1] if len(e.args) > 1 else 404
            }
            
        return response