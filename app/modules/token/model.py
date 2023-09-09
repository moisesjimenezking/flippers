from .classStructure import TokenClass
from modules.user.model import Users
from flask import jsonify, request
from create_app import app
from library.VerifyToken import verifyToken
from library.gensimUtils.utils import trainProductModelDescription
import bcrypt, datetime, jwt, threading
import logging

logging.basicConfig(level=logging.DEBUG)

class Token:
    @staticmethod
    def trainProducts(user_id):
        with app.app_context():
            trainProductModelDescription(user_id)
        
    @classmethod
    def postTokenData(cls, data):
        try:
            user = Users.getUserData({"username": data.get("username")})
            if(user["status_http"] == 200):
                user = user["response"][0]
                passwd = data.get("passwd")
                    
                #* Funcion en segundo plano
                subproceso = threading.Thread(target=Token.trainProducts, args=(user["id"],))
                subproceso.start()
                                 
                if(bcrypt.checkpw(passwd.encode('utf-8'), user["passwd"].encode('utf-8'))):
                    #* Obtener la fecha y hora actual
                    now = datetime.datetime.now()

                    #* Definir la duración de expiración del token (por ejemplo, 1 hora)
                    expiration_delta = datetime.timedelta(hours=200)

                    #* Calcular la fecha y hora de expiración sumando la duración al tiempo actual
                    expiration = now + expiration_delta

                    username = user["username"].encode('utf-8')
                    username = bcrypt.hashpw(username, bcrypt.gensalt())
                    #* Crear el payload del token incluyendo el campo 'exp'
                    payloadToken = {
                        'ud'  : str(username)+"-"+str(user["id"]),
                        'up'  : user["passwd"],
                        'exp' : expiration  #* Agregar el tiempo de expiración al payload
                    }

                    #* Generar el token JWT
                    token = jwt.encode(payloadToken, app.config['SECRET_KEY'], algorithm='HS256')
                    
                    data = {
                        "user_id" : user["id"],
                        "hash"    : token,
                        "time_exp": expiration.strftime('%Y-%m-%d %H:%M:%S')
                    }
                    
                    registerToken = TokenClass.post(**data)
                    if "id" in registerToken:
                        response = {
                            "response": registerToken,
                            "status_http": 201
                        }
                    else:
                        raise Exception("Fallo cracion del token.", 401)
                else:
                    raise Exception("Credenciales incorrectas", 401)
            else:
                raise Exception("Credenciales incorrectas", 401)
            
        except Exception as e:
            response = {
                'response':{
                    'message' : e.args[0] if len(e.args) > 0 else str(e)
                },
                'status_http':e.args[1] if len(e.args) > 1 else 404
            }
            
        return response 
    
    @classmethod
    def getTokenData(cls, data):
        try:
            #* Se extrae la id del usuario desde el token
            user_logged = verifyToken()["response"]["user_id"]
                    
            token = TokenClass.getData(**{"user_id":user_logged})
            if(len(token) > 0):
                response = {
                    "response":token, 
                    "status_http": 200
                }
            else:
                raise Exception("Sin datos." , 404)
        except Exception as e:
            response = {
                'response':{
                    'message'  : e.args[0] if len(e.args) > 0 else str(e)
                },
                
                'status_http':e.args[1] if len(e.args) > 1 else 404
            }
            
        return response 

    @classmethod
    def getRefreshTokenData(cls, data):
        try:
            #* Se extrae la id del usuario desde el token
            user_logged = verifyToken()
            logging.debug(str(user_logged))
            logging.debug(str(data))
            if user_logged["status_http"] == 200:
                user_logged = ["response"]["user_id"]
            else:
                if "user_id" in data:
                    user_logged = data["user_id"]
                else:
                    raise Exception("El usuario no pudo ser encontrado.")
               
            user = Users.getUserData({"id": user_logged})
            if(user["status_http"] == 200):
                user = user["response"][0]
                passwd = user["passwd"] 
            
                #* Obtener la fecha y hora actual
                now = datetime.datetime.now()

                #* Definir la duración de expiración del token (por ejemplo, 1 hora)
                expiration_delta = datetime.timedelta(hours=200)

                #* Calcular la fecha y hora de expiración sumando la duración al tiempo actual
                expiration = now + expiration_delta

                username = user["username"].encode('utf-8')
                username = bcrypt.hashpw(username, bcrypt.gensalt())
                #* Crear el payload del token incluyendo el campo 'exp'
                payloadToken = {
                    'ud'  : str(username)+"-"+str(user["id"]),
                    'up'  : passwd,
                    'exp' : expiration  #* Agregar el tiempo de expiración al payload
                }

                #* Generar el token JWT
                token = jwt.encode(payloadToken, app.config['SECRET_KEY'], algorithm='HS256')
                
                data = {
                    "user_id" : user["id"],
                    "hash"    : token,
                    "time_exp": expiration.strftime('%Y-%m-%d %H:%M:%S')
                }
                
                registerToken = TokenClass.postRefresh(**data)
                if "id" in registerToken:
                    response = {
                        "response": registerToken,
                        "status_http": 201
                    }
                else:
                    raise Exception("Fallo cracion del token.", 401)
            else:
                raise Exception("Credenciales incorrectas", 401)
        except Exception as e:
            response = {
                'response':{
                    'message'  : e.args[0] if len(e.args) > 0 else str(e)
                },
                
                'status_http':e.args[1] if len(e.args) > 1 else 404
            }
            
        return response 