from .classStructure import ChatterInteractionClass
from modules.bots.classStructure import BootsClass
from create_app import app
# from unidecode import unidecode

class ChatterInteraction:
        
    @classmethod
    def postChatterInteraction(cls, data):
        try:
            #boot BootsClass
            bot = BootsClass.getDataFirst(data["bot_name"])
            if bot is None:
                raise Exception("Bot no encontrado")
            
            data.pop("bot_name")
            data.update({"bot_id":bot.id})
            
            # if 'response' in data:
            #     data["response"] = unidecode.data["response"]
                
            # if 'question' in data:
            #     data["question"] = unidecode.data["question"]
                
            response = ChatterInteractionClass.postData(**data)
            response = {
                "response": "Fallo al crear la compra." if len(response) == 0 else response[0], 
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