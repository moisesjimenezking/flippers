from .classStructure import CompanyClass
from modules.bots.model import Bots
from modules.user.model import Users
import logging

logging.basicConfig(level=logging.DEBUG)
class Company:
    
    @classmethod
    def getDirection(cls, data):
        try:
            consultbot = {"name":data["bot_name"]}
            bot = Bots.getBootsData(consultbot)
            if bot["status_http"] != 200:
                raise Exception("Dirección no disponible", 400)
            
            consultUser = Users.getUserData({"id":bot["response"][0]["user_id"]})
            logging.debug(consultUser)
            if consultUser["status_http"] != 200:
                raise Exception("Dirección no disponible")   
            
            if consultUser["response"][0]["company_id"] is None:
                raise Exception("Dirección no disponible", 400)
            
            response = CompanyClass.getData(**{"id":consultUser["response"][0]["company_id"]})

            if(len(response) == 0 or response[0]["direction"] is None):
                raise Exception("Dirección no disponible", 400)
            else:
                response = {
                    "response":{
                        "message":response[0]["direction"]
                    },
                    "status_http": 200
                }
                
                response = {
                    'response':{
                        'message': response[0]["direction"],
                        'error' : None,
                        'details' : list(),
                        "note": None
                    },
                    
                    'status_http':e.args[1] if len(e.args) > 1 else 404
                }
                
        except Exception as e:
            response = {
                'response':{
                    'message': None,
                    'error' : e.args[0] if len(e.args) > 0 else str(e),
                    'details' : list(),
                    "note": None
                },
                
                'status_http':e.args[1] if len(e.args) > 1 else 404
            }
        
        return response
    
    
    @classmethod
    def getBusiness(cls, data):
        try:
            response = Users.getUserAllData(dict())
        except Exception as e:
            response = {
                "response":{
                    "message": e.args[0] if len(e.args) > 0 else str(e)
                }, 
                "status_http": e.args[1] if len(e.args) > 1 else 404
            }
        
        return response