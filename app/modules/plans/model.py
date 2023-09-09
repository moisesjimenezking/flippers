from .classStructure import PlansClass
from flask import jsonify, request

class Plans:
    
    @classmethod
    def getPlansData(cls, data):
        try:
            response = PlansClass.getData(**data)
            if(len(response) == 0):
                raise Exception("Sin datos.", 404)
            else:
                response = {"response":response, "status_http": 200}
        except Exception as e:
            response = {
                "response":{
                    "message": e.args[0] if len(e.args) > 0 else str(e)
                }, 
                "status_http": e.args[1] if len(e.args) > 1 else 404
            }
        
        return response