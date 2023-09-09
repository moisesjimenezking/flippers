from flask import render_template, jsonify, request
from create_app import app
from .model import Company
from modules.user.model import UserClass

#
#* Metodo encargador de listar los usuarios registrados
#? GET /service
#
#
@app.route('/business', methods=['GET'])
def getBusiness():
    try:
        try:
            data = request.args or request.values or request.form or request.json
            data = data = data.copy()
        except:
            data = dict()
        
        response = Company.getBusiness(data)
    except Exception as e:
        response = {
            "response":{
                "message":str(e)
            }, 
            "status_http": 404
        }
    
    return response["response"], response["status_http"]