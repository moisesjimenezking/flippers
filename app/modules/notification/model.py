from .classStructure import NotificationClass 
from library.Email import sendEmail
from .statusCodes import Code
from library.boto import boto
from library.VerifyToken import verifyToken
import logging, re, bcrypt, random

logging.basicConfig(level=logging.DEBUG)


class Notification:
    
    @classmethod
    def getNotificationData(cls, data):
        try:
            user_logged = verifyToken()
            if user_logged["status_http"] == 200:
                data.update({"user_id":user_logged["response"]["user_id"]})
                
            response = NotificationClass.getData(**data)
            if(len(response) == 0):
                raise Exception("Sin datos.", 404)
            else:
                response = {
                    "response":response, 
                    "status_http": 200
                }
        except Exception as e:
            response = {
                'response':{
                    'message'  : e.args[0] if len(e.args) > 0 else str(e)
                },
                'status_http':e.args[1] if len(e.args) > 1 else 500
            }
        
        return response
    
    @classmethod
    def putNotificationView(cls, data):
        try:
            notification = NotificationClass.getDataFirstPut(data["id"])
            
            if notification is None:
                raise Exception("Notificacion no encontrada.", 404)
            
            if notification.status_id == 2:
                setattr(notification, "status_id", 1)
                response = NotificationClass.putData(notification)
                
                response = {
                    "response"    : response,
                    "status_http" : 200
                }
            else:
                raise Exception("Notificacion no activa.", 404)
        except Exception as e:
            response = {
                'response':{
                    'message'  : e.args[0] if len(e.args) > 0 else str(e)
                },
                'status_http':e.args[1] if len(e.args) > 1 else 500
            }
        
        return response