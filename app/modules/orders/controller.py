from flask import jsonify, request
from create_app import app
from . import model
# from modules.user.paramValidation import ParamValidation


#* Se asigna importación del módulo user a variable UserModel
OrdersModel = model.Orders


#* Método encargado de listar los usuarios registrados
#? GET /users
#
@app.route('/orders', methods=['GET'])
def getOrders():
    try:

        #* Se obtiene la data de caso de estar vacía data se genera un objeto vacío
        try:
            data = request.args or request.values or request.form or request.json
            data = data.copy()
        except:
            data = dict()
            
        # #* Se validan los parámetros enviados y el token
        # validation = ParamValidation.ValidationParam(data, '/getUser')
        # if validation["status_http"] != 200:
        #     raise Exception(validation["response"]["message"], validation["status_http"])
        
        #* Se realiza la petición del GET de usuario
        response = OrdersModel.getData(data)
    except Exception as e:
        #* Se capturan las excepciones y su estatus en caso de no existir se usa 404 por defecto
        response = {
            'response':{
                'message'  : e.args[0] if len(e.args) > 0 else str(e)
            },
            
            'status_http':e.args[1] if len(e.args) > 1 else 404
        }
        
    return jsonify(response["response"]), response["status_http"]




#* Método encargado de actualizar usuarios
#? PUT /user
#
@app.route('/orders', methods=['PUT'])
def putOrders():
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
        response = OrdersModel.putData(data)
    except Exception as e:
        #* Se capturan las excepciones y su estatus en caso de no existir se usa 404 por defecto
        response = {
            'response':{
                'message'  : e.args[0] if len(e.args) > 0 else str(e)
            },
            
            'status_http':e.args[1] if len(e.args) > 1 else 404
        }
            
    return jsonify(response["response"]), response["status_http"]