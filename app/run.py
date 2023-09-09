from create_app                   import app
from flask                        import jsonify
from modules.user                 import controller   #? UserController
from modules.token                import controller   #? TokenController
from modules.plans                import controller   #? PlansController
from modules.subscriptions        import controller   #? SubscriptionsController
from modules.sales                import controller   #? SalesController
from modules.commands             import controller   #? CommandsController
from modules.bots                 import controller   #? BootsController
from modules.chatterInteraction   import controller   #? chatterInteractionController
from modules.product              import controller   #? productController
from modules.orders               import controller   #? ordersController
from modules.chatters             import controller   #? chattersController
from modules.claims               import controller   #? claimsController
from modules.company              import controller   #? companyController
from modules.notification         import controller   #? notificationController
from modules.conversation_message import controller   #? conversationMessageController
from modules.conversation         import controller   #? conversation

@app.route('/', methods=['GET'])
def hello():
    return jsonify({"message": "hello Juan!"}), 200

@app.route('/api/v1/healthcheck', methods=['GET'])
def healthcheck():
    return jsonify({"message": "OK"}), 200

@app.route('/conditions', methods=['GET'])
def conditions():
    return jsonify({"message": "En este método irán los términos y condiciones del producto Flippo."}), 200


#TODO: Se inicia la aplicacion
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
    # app.run(debug=False, host='localhost', threaded=True, ssl_context=('certs/cert.pem', 'certs/key.pem'))