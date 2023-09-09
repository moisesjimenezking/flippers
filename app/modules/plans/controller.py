from flask import render_template, jsonify, request
from create_app import app
from . import model


#* Se asigana importacion del modulo user a variable UserModel
PlansModel = model.Plans

#
#* Metodo encargador de listar los usuarios registrados
#? GET /service
#
#
@app.route('/plans', methods=['GET'])
def getPlans():
    try:
        try:
            data = request.args or request.values or request.form or request.json
            data = data = data.copy()
        except:
            data = dict()
            
        response = PlansModel.getPlansData(data)
    except:
        response = {"response":{"message":"Invalid Data"}, "status_http": 404}
    
    return jsonify(response["response"]), response["status_http"]