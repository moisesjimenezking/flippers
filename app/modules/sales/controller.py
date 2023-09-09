from flask import render_template, jsonify, request
from create_app import app
from .model import Sales
from .paramValidation import ParamValidation
import logging

logging.basicConfig(level=logging.DEBUG)

#
#* Metodo encargador de listar los usuarios registrados
#? GET /service
#
#
@app.route('/sales', methods=['GET'])
def sales():
    try:
        try:
            data = request.args or request.values or request.form or request.json
            data = data = data.copy()
        except:
            data = dict()
            
        #* Se validan los parámetros enviados y el token
        validation = ParamValidation.ValidationParam(data, '/getSales')
        if validation["status_http"] != 200:
            raise Exception(validation["response"]["message"], validation["status_http"])
            
        response = Sales.getSalesData(data)
    except Exception as e:
        response = {
            'response':{
                'message'  : e.args[0] if len(e.args) > 0 else str(e)
            },        
            'status_http':e.args[1] if len(e.args) > 1 else 404
        }
    
    return jsonify(response["response"]), response["status_http"]

#
#* Metodo encargador de listar los usuarios registrados
#? GET /service
#
#
@app.route('/sales', methods=['POST'])
def postsales():
    try:
        try:
            data = request.args or request.values or request.form or request.json
            data = data = data.copy()
        except:
            data = dict()
            
        #* Se validan los parámetros enviados y el token
        validation = ParamValidation.ValidationParam(data, '/postSales')
        if validation["status_http"] != 200:
            raise Exception(validation["response"]["message"], validation["status_http"])
        
        response = Sales.postSalesData(data)
    except Exception as e:
        response = {
            'response':{
                'message'  : e.args[0] if len(e.args) > 0 else str(e)
            },        
            'status_http':e.args[1] if len(e.args) > 1 else 404
        }
    
    return jsonify(response["response"]), response["status_http"]

#
#* Metodo encargador de listar los usuarios registrados
#? GET /service
#
#
@app.route('/sales/lastdays', methods=['GET'])
def lastdays():
    try:
        try:
            data = request.args or request.values or request.form or request.json
            data = data = data.copy()
        except:
            data = dict()
            
        #* Se validan los parámetros enviados y el token
        validation = ParamValidation.ValidationParam(data, '/getLastdays')
        logging.debug(validation)
        if validation["status_http"] != 200:
            raise Exception(validation["response"]["message"], validation["status_http"])
        
        response = Sales.getTimeData(data)
    except Exception as e:
        response = {
            'response':{
                'message'  : e.args[0] if len(e.args) > 0 else str(e)
            },        
            'status_http':e.args[1] if len(e.args) > 1 else 404
        }
    
    return jsonify(response["response"]), response["status_http"]


#
#* Metodo encargador de listar los usuarios registrados
#? GET /service
#
#
@app.route('/sales', methods=['PUT'])
def putSales():
    try:
        try:
            data = request.args or request.values or request.form or request.json
            data = data = data.copy()
        except:
            data = dict()
            
        #* Se validan los parámetros enviados y el token
        validation = ParamValidation.ValidationParam(data, '/putSales')
        logging.debug(validation)
        if validation["status_http"] != 200:
            raise Exception(validation["response"]["message"], validation["status_http"])
        
        response = Sales.putSalesData(data)
    except Exception as e:
        response = {
            'response':{
                'message'  : e.args[0] if len(e.args) > 0 else str(e)
            },        
            'status_http':e.args[1] if len(e.args) > 1 else 404
        }
    
    return jsonify(response["response"]), response["status_http"]

