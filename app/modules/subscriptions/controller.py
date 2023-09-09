from flask import render_template, jsonify, request
from create_app import app
from . import model
from modules.subscriptions.paramValidation import ParamValidation



#* Se asigana importacion del modulo user a variable UserModel
SubscriptionsModel = model.Subscriptions

#
#* Metodo encargador de registrar nuevos usuarios
#? POST /service
#
#
@app.route('/subscriptions', methods=['POST'])
def postSubscriptions():
    try:
        try:
            data = request.args or request.values or request.form or request.json
            data = data = data.copy()
        except:
            raise Exception("No se subministraron datos.", 400)

        
        validation = ParamValidation.ValidationParam(data, '/postSubscriptions')
        if validation["status_http"] != 200:
            raise Exception(validation["response"]["message"], validation["status_http"])
        
        response = SubscriptionsModel.postSubscriptionsData(data)
    except Exception as e:
        response = {
            'response':{
                'message': 'Se produjo un error',
                'error'  : e.args[0] if len(e.args) > 0 else str(e)
            },
            
            'status_http':e.args[1] if len(e.args) > 1 else 404
        }
        
    return jsonify(response["response"]), response["status_http"]

#
#* Metodo encargador de registrar nuevos usuarios
#? POST /service
#
#
@app.route('/subscriptions', methods=['GET'])
def getSubscriptions():
    try:
        try:
            data = request.args or request.values or request.form or request.json
            data = data = data.copy()
        except:
            data = dict()

        validation = ParamValidation.ValidationParam(data, '/getSubscriptions')
        if validation["status_http"] != 200:
            raise Exception(validation["response"]["message"], validation["status_http"])
        
        response = SubscriptionsModel.getSubscriptionsData(data)
    except Exception as e:
        response = {
            'response':{
                'message': 'Se produjo un error',
                'error'  : e.args[0] if len(e.args) > 0 else str(e)
            },
            
            'status_http':e.args[1] if len(e.args) > 1 else 404
        }
        
    return jsonify(response["response"]), response["status_http"]