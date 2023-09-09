from flask import render_template, jsonify, request
from create_app import app
from . import model
from modules.token.paramValidation import ParamValidation
import json
from werkzeug.utils import secure_filename
from werkzeug.datastructures import ImmutableMultiDict
from werkzeug.formparser import parse_form_data

#* Se asigna importación del módulo token a variable TokenModel
TokenModel = model.Token


#* Metodo encargador de generar el token
#? POST /service
#
@app.route('/token', methods=['POST'])
def postToken():
    try:
        try:
            data = request.args or request.values or request.form or request.json
            data = data = data.copy()
        except:
            raise Exception("No se suministraron datos.", 400)
        
        if('password' in data):
            data.update({"passwd":data.get("password")})
            data.pop("password")
        
        validation = ParamValidation.ValidationParam(data, '/postToken')
        if validation["status_http"] != 200:
            raise Exception(validation["response"]["message"], validation["status_http"])
        
        response = TokenModel.postTokenData(data)
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
#* Método encargado de vizualizar los tokens de un afiliado
#? POST /service
#
#
@app.route('/token', methods=['GET'])
def getToken():
    try:
        try:
            data = request.args or request.values or request.form or request.json
            data = data.copy()
        except:
            data = dict()

        validation = ParamValidation.ValidationParam(data, '/getToken')
        if validation["status_http"] != 200:
            raise Exception(validation["response"]["message"], validation["status_http"])
        
        response = TokenModel.getTokenData(data)
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
#* Método encargado de vizualizar los tokens de un afiliado
#? POST /service
#
#
@app.route('/refresh_token', methods=['POST'])
def getRefreshToken():
    try:
        try:
            data = request.args or request.values or request.form or request.json
            data = data.copy()
        except:
            data = dict()

        # validation = ParamValidation.ValidationParam(data, '/getRefreshToken')
        # if validation["status_http"] != 200:
        #     raise Exception(validation["response"]["message"], validation["status_http"])
        
        response = TokenModel.getRefreshTokenData(data)
    except Exception as e:
        response = {
            'response':{
                'message': 'Se produjo un error',
                'error'  : e.args[0] if len(e.args) > 0 else str(e)
            },
            
            'status_http':e.args[1] if len(e.args) > 1 else 404
        }
        
    return jsonify(response["response"]), response["status_http"]