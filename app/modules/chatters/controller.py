from flask import jsonify, request
from create_app import app
from . import model
from modules.sales.model import Sales
from .paramValidation import ParamValidation


#* Se asigna importación del módulo user a variable UserModel
ChattersModel = model.Chatters


#* Método encargado de listar los usuarios registrados
#? GET /users
#
@app.route('/chatters', methods=['GET'])
def getChatters():
    try:
        #* Se obtiene la data de caso de estar vacía data se genera un objeto vacío
        try:
            data = request.args or request.values or request.form or request.json
            data = data.copy()
        except:
            data = dict()
            
        #* Se validan los parámetros enviados y el token
        validation = ParamValidation.ValidationParam(data, '/getChatters')
        if validation["status_http"] != 200:
            raise Exception(validation["response"]["message"], validation["status_http"])
        
        #* Se realiza la petición del GET de usuario
        response = Sales.getChattersData(data)
    except Exception as e:
        #* Se capturan las excepciones y su estatus en caso de no existir se usa 404 por defecto
        response = {
            'response':{
                'message': 'Se produjo un error',
                'error'  : e.args[0] if len(e.args) > 0 else str(e)
            },
            
            'status_http':e.args[1] if len(e.args) > 1 else 404
        }
        
    return jsonify(response["response"]), response["status_http"]


#* Método encargado de listar los usuarios registrados
#? GET /users
#
@app.route('/chatters/list_black', methods=['GET'])
def getListBlack():
    try:
        #* Se obtiene la data de caso de estar vacía data se genera un objeto vacío
        try:
            data = request.args or request.values or request.form or request.json
            data = data.copy()
        except:
            data = dict()
            
        # #* Se validan los parámetros enviados y el token
        # validation = ParamValidation.ValidationParam(data, '/getChatters')
        # if validation["status_http"] != 200:
        #     raise Exception(validation["response"]["message"], validation["status_http"])
        
        #* Se realiza la petición del GET de usuario
        response = ChattersModel.getListBlack(data)
    except Exception as e:
        #* Se capturan las excepciones y su estatus en caso de no existir se usa 404 por defecto
        response = {
            'response':{
                'message': 'Se produjo un error',
                'error'  : e.args[0] if len(e.args) > 0 else str(e)
            },
            
            'status_http':e.args[1] if len(e.args) > 1 else 404
        }
        
    return jsonify(response["response"]), response["status_http"]

#* Método encargado de actualizar usuarios
#? PUT /user
#
@app.route('/chatters', methods=['PUT'])
def putChatters():
    try:
        #* Se obtiene la data de caso de estar vacía data se genera una excepción
        try:
            data = request.args or request.values or request.form or request.json
            data = data.copy()
        except:
            raise Exception("No se subministraron datos.", 400)
            
        # #* Se validan los parámetros enviados y el token
        # validation = ParamValidation.ValidationParam(data, '/putUser')
        # if validation["status_http"] != 200:
        #     raise Exception(validation["response"]["message"], validation["status_http"])
        
        #* Se realiza la petición del PUT de usuario
        response = ChattersModel.putData(data)
    except Exception as e:
        #* Se capturan las excepciones y su estatus en caso de no existir se usa 404 por defecto
        response = {
            'response':{
                'message': 'Se produjo un error',
                'error'  : e.args[0] if len(e.args) > 0 else str(e)
            },
            
            'status_http':e.args[1] if len(e.args) > 1 else 404
        }
            
    return jsonify(response["response"]), response["status_http"]


#* Método encargado de listar los usuarios registrados
#? GET /users
#
@app.route('/chatters/list', methods=['GET'])
def getChattersList():
    try:
        #* Se obtiene la data de caso de estar vacía data se genera un objeto vacío
        try:
            data = request.args or request.values or request.form or request.json
            data = data.copy()
        except:
            data = dict()
            
        # #* Se validan los parámetros enviados y el token
        validation = ParamValidation.ValidationParam(data, '/getchattersList')
        if validation["status_http"] != 200:
            raise Exception(validation["response"]["message"], validation["status_http"])
        
        #* Se realiza la petición del GET de usuario
        response = ChattersModel.getDataList(data)
    except Exception as e:
        #* Se capturan las excepciones y su estatus en caso de no existir se usa 404 por defecto
        response = {
            'response':{
                'message': 'Se produjo un error',
                'error'  : e.args[0] if len(e.args) > 0 else str(e)
            },
            
            'status_http':e.args[1] if len(e.args) > 1 else 404
        }
        
    return jsonify(response["response"]), response["status_http"]