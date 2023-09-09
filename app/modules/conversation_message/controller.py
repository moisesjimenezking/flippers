from flask import jsonify, request
from create_app import app
from .model import ConversationMessage
from .paramValidation import ParamValidation
import logging, json

logging.basicConfig(level=logging.DEBUG)

#* Método encargado de listar los usuarios registrados
#? GET /users
#
@app.route('/conversation_message', methods=['POST'])
def postConversationMessage():
    try:
        #* Se obtiene la data de caso de estar vacía data se genera un objeto vacío
        try:
            data = request.args or request.values or request.form or request.json
            data = data.copy()
        except:
            raise Exception("No se subministraron datos.", 400)
            
        #* Se validan los parámetros enviados y el token
        validation = ParamValidation.ValidationParam(data, '/postConversationMessage')
        if validation["status_http"] != 200:
            raise Exception(validation["response"]["message"], validation["status_http"])
        
        #* Se realiza la petición del GET de usuario
        response = ConversationMessage.postConversationMessage(data)
    except Exception as e:
        #* Se capturan las excepciones y su estatus en caso de no existir se usa 404 por defecto
        response = {
            'response':{
                'message'  : e.args[0] if len(e.args) > 0 else str(e)
            },
            
            'status_http':e.args[1] if len(e.args) > 1 else 404
        }
        
    return jsonify(response["response"]), response["status_http"]

#* Método encargado de listar los usuarios registrados
#? GET /users
#
@app.route('/conversation/new_message', methods=['POST'])
def postConversationApp():
    try:
        #* Se obtiene la data de caso de estar vacía data se genera un objeto vacío
        try:
            data = request.args or request.values or request.form or request.json
            data = data.copy()
        except:
            raise Exception("No se subministraron datos.", 400)
            
        payload_data = json.loads(data["payload"])
        data["message"] = payload_data["message"]
        data["status"] = payload_data["status"]
        data.pop("payload")
        

        logging.debug(str(data))
        
        #* Se validan los parámetros enviados y el token
        validation = ParamValidation.ValidationParam(data, '/postConversationResponse')
        if validation["status_http"] != 200:
            raise Exception(validation["response"]["message"], validation["status_http"])
        
        #* Se realiza la petición del GET de usuario
        response = ConversationMessage.postConversationApp(data)
    except Exception as e:
        #* Se capturan las excepciones y su estatus en caso de no existir se usa 404 por defecto
        response = {
            'response':{
                'message'  : e.args[0] if len(e.args) > 0 else str(e)
            },
            
            'status_http':e.args[1] if len(e.args) > 1 else 400
        }
        
    return jsonify(response["response"]), response["status_http"]