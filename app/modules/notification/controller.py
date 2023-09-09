from flask import jsonify, request
from create_app import app
from .model import Notification
from modules.user.paramValidation import ParamValidation
import logging

logging.basicConfig(level=logging.DEBUG)

#* Método encargado de listar los usuarios registrados
#? GET /notification
#
@app.route('/notification', methods=['GET'])
def getNotificationData():
    try:
        #* Se obtiene la data de caso de estar vacía data se genera un objeto vacío
        try:
            data = request.args or request.values or request.form or request.json
            data = data.copy()
        except:
            data = dict()
            
        #* Se validan los parámetros enviados y el token
        # validation = ParamValidation.ValidationParam(data, '/getUser')
        # if validation["status_http"] != 200:
        #     raise Exception(validation["response"]["message"], validation["status_http"])
        
        #* Se realiza la petición del GET de usuario
        response = Notification.getNotificationData(data)
    except Exception as e:
        #* Se capturan las excepciones y su estatus en caso de no existir se usa 404 por defecto
        response = {
            'response':{
                'message': 'Se produjo un error',
                'error'  : e.args[0] if len(e.args) > 0 else str(e)
            },
            
            'status_http':e.args[1] if len(e.args) > 1 else 500
        }
        
    return jsonify(response["response"]), response["status_http"]

@app.route('/notification/view', methods=['PUT'])
def putNotificationView():
    try:
        #* Se obtiene la data de caso de estar vacía data se genera un objeto vacío
        try:
            data = request.args or request.values or request.form or request.json
            data = data.copy()
        except:
            data = dict()
            
        #* Se validan los parámetros enviados y el token
        # validation = ParamValidation.ValidationParam(data, '/getUser')
        # if validation["status_http"] != 200:
        #     raise Exception(validation["response"]["message"], validation["status_http"])
        
        #* Se realiza la petición del GET de usuario
        response = Notification.putNotificationView(data)
    except Exception as e:
        #* Se capturan las excepciones y su estatus en caso de no existir se usa 404 por defecto
        response = {
            'response':{
                'message': 'Se produjo un error',
                'error'  : e.args[0] if len(e.args) > 0 else str(e)
            },
            
            'status_http':e.args[1] if len(e.args) > 1 else 500
        }
        
    return jsonify(response["response"]), response["status_http"]