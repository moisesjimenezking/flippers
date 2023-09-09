from flask import render_template, jsonify, request
from create_app import app
from modules.sales.model import Sales
from modules.product.model import Product
from modules.chatters.model import Chatters
from modules.company.model import Company
from .model import Commands
from modules.tickets.model import Tickets
from .paramValidation import ParamValidation
import logging

logging.basicConfig(level=logging.DEBUG)

#
#* Metodo encargador de listar los usuarios registrados
#? GET /service
#
#
@app.route('/commands', methods=['GET'])
def getCommands():
    try:
        try:
            data = request.args or request.values or request.form or request.json
            data = data = data.copy()
        except:
            raise Exception("No se subministraron datos.", 400)
        
        response = Commands.getCommands(data)
    except Exception as e:
        response = {"response":{"message":str(e)}, "status_http": 404}
    
    return jsonify(response["response"]), response["status_http"]



#
#* Metodo encargador de listar los usuarios registrados
#? GET /service
#
#
@app.route('/commands', methods=['POST'])
def postCommands():
    try:
        try:
            data = request.args or request.values or request.form or request.json
            data = data = data.copy()
        except:
            data = dict()

        #* Se validan los parámetros enviados y el token
        validation = ParamValidation.ValidationParam(data, '/postCommands')
        if validation["status_http"] != 200:
            raise Exception(validation["response"]["message"], validation["status_http"])
        
        response = Commands.postCommands(data)
    except Exception as e:
        response = {"response":{"message":str(e)}, "status_http": 404}
    
    return jsonify(response["response"]), response["status_http"]

#
#* Metodo encargador de listar los usuarios registrados
#? GET /service
#
#
@app.route('/commands', methods=['PUT'])
def putCommands():
    try:
        try:
            data = request.args or request.values or request.form or request.json
            data = data = data.copy()
        except:
            data = dict()

        response = Commands.putCommands(data)
    except Exception as e:
        response = {"response":{"message":str(e)}, "status_http": 404}
    
    return jsonify(response["response"]), response["status_http"]

#
#* Metodo encargador de listar los usuarios registrados
#? GET /service
#
#
@app.route('/commands/all', methods=['GET'])
def getAll():
    try:
        try:
            data = request.args or request.values or request.form or request.json
            data = data = data.copy()
        except:
           data = dict()
        
        response = Commands.getCommandsApp(data)
    except Exception as e:
        response = {"response":{"message":str(e)}, "status_http": 404}
    
    return jsonify(response["response"]), response["status_http"]

#
#* Metodo encargador de listar los usuarios registrados
#? GET /service
#
#
@app.route('/commands/action', methods=['POST'])
def getAction():
    try:
        try:
            data = request.args or request.values or request.form or request.json
            data = data = data.copy()
        except:
            raise Exception("No se subministraron datos.", 400)
        
        if data["code"].upper() in {"COMPRAR","DELIVERY"}:
            response = Sales.postBotData(data)
        elif data["code"].upper() in {"PRECIOS","DETALLES","PRODUCTOS"}:
            response = Product.getProductBotPrice(data)
        elif data["code"].upper() in {"UBICACION","UBICACIÓN"}:
            response = Company.getDirection(data)
            if response["status_http"] != 200:
                aux = Commands.getCommands(data)
                if aux["status_http"] == 200:
                    response = aux
        elif data["code"].upper() in {"TICKET"}:
            response = Tickets.postDataBot(data)
        else:
            response = Commands.getCommands(data)

    except Exception as e:
        response = {
            'response':{
                'message': None,
                'error' : e.args[0] if len(e.args) > 0 else str(e),
                'details' : list(),
                "error": None
            },
            "status_http": e.args[1] if len(e.args) > 1 else 404
        }
    
    return jsonify(response["response"]), response["status_http"]


#* Método encargado de actualizar usuarios
#? PUT /user
#
@app.route('/commands', methods=['DELETE'])
def deleteCommands():
    try:
        #* Se obtiene la data de caso de estar vacía data se genera una excepción
        try:
            data = request.args or request.values or request.form or request.json
            data = data.copy()
        except:
            data = dict()
            
        # #* Se validan los parámetros enviados y el token
        # validation = ParamValidation.ValidationParam(data, '/deletedCommands')
        # if validation["status_http"] != 200:
        #     raise Exception(validation["response"]["message"], validation["status_http"])
        
        #* Se realiza la petición del PUT de usuario
        response = Commands.deleteCommand(data)
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