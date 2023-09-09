from .classStructure import ConversationClass
from library.boto import boto
from modules.bots.classStructure import BootsClass
from modules.chatters.classStructure import ChattersClass
from library.VerifyToken import verifyToken
from modules.conversation.statusCodes import Code
import logging, re

logging.basicConfig(level=logging.DEBUG)

class Conversation:
    @classmethod
    def getConversation(cls, data):
        try:
            #* Se extraen las ventas del usuario loggeado
            user_logged = verifyToken()["response"]["user_id"]
            
            #* Se extrae el bot apartir del usuario
            bot = BootsClass.getDataFirstUser(user_logged)
            
            searchConversation = dict()
            if "id" in data:
                searchConversation.update({"id": data["id"]})
                
            #* Status de la conversacion
            if "status" in data:
                searchConversation.update({"status_id":Code(data["status"])})
                           
            #* Chatters mediante su nombre
            if "chatter_name" in data and "chatter_phone" not in data:
                chatter_id_list = ChattersClass.getChattersLike(data["chatter_name"])
            
            #* Chatter mediante sun phone
            if "chatter_phone" in data and "chatter_name" not in data:
                chatter_id_list = ChattersClass.getChattersLike(data["chatter_phone"])
            
            if "chatter_id" in data and "chatter_name" not in data and "chatter_phone" not in data:
                chatter_id_list = [data["chatter_id"]]
                
            if "chatter_id_list" in locals() and len(chatter_id_list) > 0:
                response = ConversationClass.getDataAll(chatter_id_list, **searchConversation)
            else:
                response = ConversationClass.getDataAll(**searchConversation)
            
            if len(response) > 0:
                response = {
                    "response":response,
                    "status_http": 200
                }
            else:
                raise Exception("Sin conversaciones.", 404)

        except Exception as e:
            response = {
                'response':{
                    'message'  : e.args[0] if len(e.args) > 0 else str(e)
                },
                
                'status_http':e.args[1] if len(e.args) > 1 else 404
            }
        
        return response
    