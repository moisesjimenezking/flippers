from .classStructure import SubscriptionsClass
from modules.user.model import Users
from modules.plans.model import Plans
from flask import jsonify, request
from create_app import app
import bcrypt
import datetime

class Subscriptions:
    
    #* Metodo para crear subscripciones
    @classmethod
    def postSubscriptionsData(cls, data):
        try:
            #* Se consulta los datos del usuario.
            user = Users.getUserData({})
            
            #* Se consulta los datos del plan.
            plans = Plans.getPlansData({"code": data.get("code")}) if "code" in data else Plans.getPlansData({"id": data.get("plan_id")})
            
            #* En caso de que no se encuentre el usuario o el plan
            if(user["status_http"] != 200 or plans["status_http"] != 200):
                message = user["response"]["error"] if user["status_http"] is not 200 else plans["response"]["error"]
                raise Exception(message)
            
            #* Se verifica si el usuario ya posse una subscricion
            registerOld = SubscriptionsClass.getDataFirst(user["response"][0]["id"])

            #* Obtener la fecha y hora actual
            datetime_start = datetime.datetime.now()
            durationsDays = datetime.timedelta(days=30)
            datetime_end = datetime_start + durationsDays
                
            #* De existir un registro se procede a actualizar
            if registerOld is not None:
                update = {
                    'id'             : registerOld.id,
                    "plans_id"       : plans["response"][0]["id"],
                    "datetime_start" : datetime_start.strftime('%Y-%m-%d %H:%M:%S'),
                    "datetime_end"   : datetime_end.strftime('%Y-%m-%d %H:%M:%S'),
                    "status_id"      : 2
                }
   
                response = SubscriptionsClass.putData(update)
                if "id" not in response:
                    raise Exception("Fallo en la actualizacion.")
                
                response = {
                    "response": response, 
                    "status_http": 201,
                }
            else:
                data = {
                    "user_id"     : user["response"][0]["id"],
                    "plans_id"    : plans["response"][0]["id"],
                    "datetime_end": datetime_end.strftime('%Y-%m-%d %H:%M:%S')
                }
                
                response = SubscriptionsClass.postData(**data)
                if len(response) == 0:
                    raise Exception("Fallo al crear la subscripcion.")
                
                response = {
                    "response": response[0], 
                    "status_http": 201
                }
                
        except Exception as e:
            response = {
                'response':{
                    'message': e.args[0] if len(e.args) > 0 else str(e)
                },
                'status_http':e.args[1] if len(e.args) > 1 else 404
            }
            
        return response 
    
    @classmethod
    def getSubscriptionsData(cls, data):
        try:
            #* Si el username viene en la data se consulta los datos del usuario.
            if("username" in data):
                user = Users.getUserData({"username": data.get("username")})
                data.pop("username")
                
                if(user["status_http"] == 200):
                    data.update({"user_id":user["response"][0]["id"]})
                else:
                    raise Exception("El usuario no fue encontrado.")
            
            #* Si el code viene en la data se consulta los datos del plan.
            if("code" in data):
                plans = Plans.getPlansData({"code": data.get("code")})
                data.pop("code")
                
                if(plans["status_http"] == 200):
                    data.update({"plans_id":plans["response"][0]["id"]})
                else:
                    raise Exception("El plan no fue encontrado.")
                
            response = SubscriptionsClass.getData(**data)
            if(len(response) == 0):
                raise Exception("Sin datos.", 404)
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
