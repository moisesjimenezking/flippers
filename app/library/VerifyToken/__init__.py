import jwt
from create_app import app
from flask import request
import logging

logging.basicConfig(level=logging.DEBUG)

def verifyToken():
    try:
        auth_header = request.headers.get('Authorization')
        if auth_header and auth_header.startswith('Bearer '):
            token = auth_header.split(' ')[1]
            payload = jwt.decode(token, app.config['SECRET_KEY'], algorithms=['HS256'])
            
            response = {
                "response":{
                    "result":"Ok",
                    "payload":payload,
                    "user_id":int(payload["ud"].split("-")[-1])
                }, 
                "status_http":200
            }
        else:
            raise Exception("Metodo requiere token")
            
    except jwt.ExpiredSignatureError as e:
        response = {
            'response':{
                'message': 'Token expirado',
                'error'  : str(e)
            },
            'status_http': 401
        }
    except jwt.InvalidTokenError as e:
        response = {
            'response':{
                'message': 'Token inválido',
                'error'  : str(e)
            },
            'status_http': 401
        }

    except Exception as e:
        response = {
            'response':{
                'message': str(e)
            },
            'status_http': 404
        }
        
    return response