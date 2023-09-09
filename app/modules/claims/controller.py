from flask import render_template, jsonify, request
from create_app import app
from .model import Claims


#* Se asigana importacion del modulo user a variable UserModel
ClaimsModel = Claims

#
#* Metodo encargador de listar los usuarios registrados
#? GET /service
#
#
@app.route('/claims', methods=['GET'])
def getClaims():
    try:
        try:
            data = request.args or request.values or request.form or request.json
            data = data = data.copy()
        except:
            data = dict()
            
        response = ClaimsModel.getData(data)

    except Exception as e:
        response = {"response":{"message":str(e)}, "status_http": 404}
    
    return jsonify(response["response"]), response["status_http"]


#
#* Metodo encargador de listar los usuarios registrados
#? GET /service
#
#
@app.route('/claims', methods=['POST'])
def postClaims():
    try:
        try:
            data = request.args or request.values or request.form or request.json
            data = data = data.copy()
        except:
            raise Exception("No se subministraron datos.", 400)

        response = ClaimsModel.postData(data)
     
    except Exception as e:
        response = {
            "response":{
                "message": e.args[0] if len(e.args) > 0 else str(e)
            }, 
            "status_http": e.args[1] if len(e.args) > 1 else 404
        }
    
    return jsonify(response["response"]), response["status_http"]
