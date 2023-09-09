from flask import jsonify, request, json
from create_app import app
from . import model
# from modules.boots.paramValidation import ParamValidation
from library.Email import sendEmail


#* Se asigna importación del módulo user a variable UserModel
BotsModel = model.Bots


#* Método encargado de listar los usuarios registrados
#? GET /users
#
@app.route('/bots', methods=['GET'])
def getBoots():
    try:
        try:
            data = request.args or request.values or request.form or request.json
            data = data.copy()
        except:
            data = dict()
            
        #* Se validan los parámetros enviados y el token
        # validation = ParamValidation.ValidationParam(data, '/getBoots')
        # if validation["status_http"] != 200:
        #     raise Exception(validation["response"]["message"], validation["status_http"])
        
        #* Se realiza la petición del GET de usuario
        response = BotsModel.getBootsData(data)
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
@app.route('/bots', methods=['POST'])
def postBoots():
    try:
        #* Se obtiene la data de caso de estar vacía data se genera una excepción
        try:
            data = request.args or request.values or request.form or request.json
            data = data.copy()
        except:
            raise Exception("No se subministraron datos.", 400)
            
        # #* Se validan los parámetros enviados y el token
        # validation = ParamValidation.ValidationParam(data, '/postUser')
        # if validation["status_http"] != 200:
        #     raise Exception(validation["response"]["message"], validation["status_http"])
        
        #* Se realiza la petición del POST de usuario
        response = BotsModel.postData(data)
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
@app.route('/bots', methods=['PUT'])
def putBoots():
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
        response = BotsModel.putData(data)
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


#* Método encargado de generar estadisticas
#? GET /users
#
@app.route('/bots/statistic', methods=['GET'])
def getStatistic():
    try:
        try:
            data = request.args or request.values or request.form or request.json
            data = data.copy()
        except:
            data = dict()
        # #* Se validan los parámetros enviados y el token
        # validation = ParamValidation.ValidationParam(data, '/putUser')
        # if validation["status_http"] != 200:
        #     raise Exception(validation["response"]["message"], validation["status_http"])
        
        response = BotsModel.getStatistic(data)
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