from flask import jsonify, request
from create_app import app
from . import model
from modules.user.paramValidation import ParamValidation
import logging

logging.basicConfig(level=logging.DEBUG)

#* Se asigna importación del módulo user a variable UserModel
UserModel = model.Users


#* Método encargado de listar los usuarios registrados
#? GET /users
#
@app.route('/user', methods=['GET'])
def getUser():
    try:
        #* Se obtiene la data de caso de estar vacía data se genera un objeto vacío
        try:
            data = request.args or request.values or request.form or request.json
            data = data.copy()
        except:
            data = dict()
            
        #* Se validan los parámetros enviados y el token
        validation = ParamValidation.ValidationParam(data, '/getUser')
        if validation["status_http"] != 200:
            raise Exception(validation["response"]["message"], validation["status_http"])
        
        #* Se realiza la petición del GET de usuario
        response = UserModel.getUserData(data)
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
@app.route('/user/all', methods=['GET'])
def getUserAll():
    try:
        #* Se obtiene la data de caso de estar vacía data se genera un objeto vacío
        try:
            data = request.args or request.values or request.form or request.json
            data = data.copy()
        except:
            data = dict()
            
        #* Se validan los parámetros enviados y el token
        validation = ParamValidation.ValidationParam(data, '/getUserAll')
        if validation["status_http"] != 200:
            raise Exception(validation["response"]["message"], validation["status_http"])
        
        #* Se realiza la petición del GET de usuario
        response = UserModel.getUserAllApp(data)
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

#* Método encargado de registrar nuevos usuarios
#? POST /user
#
@app.route('/user', methods=['POST'])
def postUser():
    try:
        #* Se obtiene la data de caso de estar vacía data se genera una excepción
        try:
            data = request.args or request.values or request.form or request.json
            data = data.copy()
        except:
            raise Exception("No se subministraron datos.", 400)
        
        #* De ser enviada la key password se cambia internamente por passwd y se elimina
        if('password' in data):
            data.update({"passwd":data.get("password")})
            data.pop("password")
            
        logging.debug(str(data))
        #* Se validan los parámetros enviados y el token
        validation = ParamValidation.ValidationParam(data, '/postUser')
        if validation["status_http"] != 200:
            raise Exception(validation["response"]["message"], validation["status_http"])
        logging.debug(str(data))
        #* Se realiza la petición del POST de usuario
        response = UserModel.postData(data)
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
@app.route('/user', methods=['PUT'])
def putUser():
    try:
        #* Se obtiene la data de caso de estar vacía data se genera una excepción
        try:
            data = request.args or request.values or request.form or request.json
            data = data.copy()
        except:
            raise Exception("No se subministraron datos.", 400)
        
        #* De ser enviada la key password se cambia internamente por passwd y se elimina
        if('password' in data):
            data["passwd"] = data["password"]
            del data["password"]
            
        #* Se validan los parámetros enviados y el token
        validation = ParamValidation.ValidationParam(data, '/putUser')
        if validation["status_http"] != 200:
            raise Exception(validation["response"]["message"], validation["status_http"])
        
        #* Se realiza la petición del PUT de usuario
        response = UserModel.putData(data)
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


#* Método encargado de generar codigos de recuperacion 
#? GET /users
#
@app.route('/user/generated_code', methods=['GET'])
def getGeneratedCode():
    try:
        try:
            data = request.args or request.values or request.form or request.json
            data = data.copy()
        except:
            raise Exception("No se subministraron datos.", 400)
            
        #* Se validan los parámetros enviados y el token
        validation = ParamValidation.ValidationParam(data, '/generated_code')
        if validation["status_http"] != 200:
            raise Exception(validation["response"]["message"], validation["status_http"])
        
        #* Se realiza la petición del GET de usuario
        response = UserModel.getGeneratedCode(data)
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
@app.route('/user', methods=['DELETE'])
def deleteUser():
    try:
        #* Se obtiene la data de caso de estar vacía data se genera una excepción
        try:
            data = request.args or request.values or request.form or request.json
            data = data.copy()
        except:
            data = dict()
            
        #* Se validan los parámetros enviados y el token
        validation = ParamValidation.ValidationParam(data, '/deletedUser')
        if validation["status_http"] != 200:
            raise Exception(validation["response"]["message"], validation["status_http"])
        
        #* Se realiza la petición del PUT de usuario
        response = UserModel.deleteUser(data)
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