from flask import render_template, jsonify, request
from create_app import app
from . import model


#* Se asigana importacion del modulo user a variable UserModel
ChatterInteractionModel = model.ChatterInteraction


#
#* Metodo encargador de listar los usuarios registrados
#? GET /service
#
#
@app.route('/chatter_interaction', methods=['POST'])
def postChatterInteraction():
    try:
        try:
            data = request.args or request.values or request.form or request.json
            data = data = data.copy()
        except:
            raise Exception("No se subministraron datos.", 400)
            
        response = ChatterInteractionModel.postChatterInteraction(data)
    except Exception as e:
        response = {"response":{"message":str(e)}, "status_http": 404}
    
    return jsonify(response["response"]), response["status_http"]
