from . import classStructure
from modules.tempCode.classStructure import TempCodeClass
from flask import jsonify, request, json
from library.Email import sendEmail
from library.goMailer.sendCode import send
from datetime import datetime, timedelta
from .statusCodes import Code
from modules.company.classStructure import CompanyClass
from modules.bots.classStructure import BootsClass
from library.boto import boto
from library.VerifyToken import verifyToken

import logging, re, bcrypt, random

logging.basicConfig(level=logging.DEBUG)

UserClass = classStructure.UserClass
# UserLogClass = classStructure.UserLogClass
class Users:
    
    @classmethod
    def getUserData(cls, data):
        try:
            user_logged = verifyToken()
            if user_logged["status_http"] == 200:
                data.update({"id":user_logged["response"]["user_id"]})
                
            response = UserClass.getData(**data)
            if(len(response) == 0):
                raise Exception("Sin datos",404)
            else:
                response = {"response":response, "status_http": 200}
        except Exception as e:
            response = {
                'response':{
                    'message'  : e.args[0] if len(e.args) > 0 else str(e)
                },
                'status_http':e.args[1] if len(e.args) > 1 else 404
            }
        
        return response
    
    @classmethod
    def getUserAllApp(cls, data):
        try:
            response = UserClass.getData(**data)
            if(len(response) == 0):
                raise Exception("Sin datos",404)
            else:
                response = {"response":response, "status_http": 200}
        except Exception as e:
            response = {
                'response':{
                    'message'  : e.args[0] if len(e.args) > 0 else str(e)
                },
                'status_http':e.args[1] if len(e.args) > 1 else 404
            }
        
        return response
    
    @classmethod
    def getUserAllData(cls, data):
        try:
            response = UserClass.getUserAllData()
            if(len(response) == 0):
                raise Exception("Sin datos",404)
            else:
                response = {"response":response, "status_http": 200}
        except Exception as e:
            response = {
                'response':{
                    'message'  : e.args[0] if len(e.args) > 0 else str(e)
                },
                'status_http':e.args[1] if len(e.args) > 1 else 404
            }
        
        return response
    
    @classmethod
    def postData(cls, data):
        try:
            #*encode password
            passwd = data.get("passwd").encode('utf-8')
            data["passwd"] = bcrypt.hashpw(passwd, bcrypt.gensalt())
            
            dataCompany = dict()
            if "company_name" in data:
                dataCompany.update({"company_name":data["company_name"]})
                data.pop("company_name")
                
                if "direction" in data:
                    dataCompany.update({"direction":data["direction"]})
                    data.pop("direction")
                    
                if "company_image_url" in data:
                    product_name = re.sub(r"[^\w\s]", "", dataCompany["company_name"]).replace(" ", "_")+"."+data["company_image_url"].split("/")[1].split(";")[0]
                    base64 = data["company_image_url"].split(",")[-1]
                    content_type = data["company_image_url"].split(":")[1].split(";")[0]
                    url = boto(dataCompany["company_name"], product_name, base64, content_type)

                    if url["status_http"] == 200:
                        dataCompany.update({"image_url":url["response"]["url"]})
                        data.pop("company_image_url")
                    else:
                        raise Exception("error url", 500)
            
            postData = UserClass.postData(**data)
            if "message" in postData:
                raise Exception(postData["message"])
            else:
                if "company_name" in dataCompany:
                    company = CompanyClass.post(**dataCompany)

                    if "id" in company:
                        user = UserClass.getDataFirstPut(postData["id"])
                        dataUpdate = {"company_id":company["id"]}
                        
                        for key, value in dataUpdate.items():
                            if hasattr(user, key): 
                                attr = getattr(user, key)
                                if str(attr) != str(value):
                                    setattr(user, key, value)
                            
                        update = UserClass.putData(user)
                        if "id" in update:
                            response = {
                                "response":update, 
                                "status_http": 201
                            }
                        else:
                            raise Exception("Error al asignar la compañia.")
                    else:
                        raise Exception("Error al crear la compañia.")
                else:
                    response = {
                        "response":UserClass.getDataFirst(postData["id"]),
                        "status_http":201
                    }
                    
        except Exception as e:
            response = {
                'response':{
                    'message'  : e.args[0] if len(e.args) > 0 else str(e)
                },
                'status_http':e.args[1] if len(e.args) > 1 else 404
            }
            
        return response
    
    @classmethod
    def putData(cls, data):
        try:
            if "id" not in data:
                user_logged = verifyToken()
                if user_logged["status_http"] == 200:
                    data.update({"id":user_logged["response"]["user_id"]})
            
            #* si el dode es enviado
            if("code" in data):
                searchCode = {
                    "user_id"   : data["id"],
                    "code"      : data["code"],
                    "status_id" : Code("AVAILABLE")
                }

                resulCode = TempCodeClass.getDataCode(**searchCode)
                if "message" in resulCode:
                    raise Exception(resulCode["message"])

                data.pop("code") 
                code = True
                
            #* si desea modificar el password se requiere el codigo enviado al correo o whatsapp
            if("passwd" in data):
                if(code == False):
                    raise Exception("El codigo es nesesario para el cambio del contraseña.")
                        
                #* encode password
                passwd = data.get("passwd").encode('utf-8')
                data["passwd"] = bcrypt.hashpw(passwd, bcrypt.gensalt())
            
            #* si desea verificar el email se requiere el codigo enviado al correo
            # if("verified_email" in data):
                # if(code == False):
                #     raise Exception("El codigo es nesesario para la verificacion del correo")
            
            
            # if "username" in data:
                # lastChange = UserLogClass.getDataFirst(data["id"], data["username"])
                # datetimeSearch = (datetime.now() - timedelta(days=120)).strftime('%Y-%m-%d')
                # datetimeLastChange = lastChange["datetime"].strftime('%Y-%m-%d')
                # if datetimeLastChange > datetimeSearch:
                #     raise Exception("El nombre de usuario solo puede ser cambiado pasado 120 días desde su última modificación", 400)
                
                
            user = UserClass.getDataFirstPut(data.get("id"))
            change = False
            
            for key, value in data.items():
                if hasattr(user, key): 
                    attr = getattr(user, key)
                    if str(attr) != str(value):
                        change =True
                        setattr(user, key, value)

            if(change):
                update = UserClass.putData(user)
                if "id" in update:
                    response = {
                        "response":update, 
                        "status_http": 201
                    }
                else:
                    raise Exception("Se ha producido un error en la actualización de los datos, por favor, espere unos minutos y vuelva a intentar.", 304)
            else:
                raise Exception("Se ha producido un error en la actualización de los datos, por favor, espere unos minutos y vuelva a intentar.", 304)
        except Exception as e:
            response = {
                'response':{
                    'message'  : e.args[0] if len(e.args) > 0 else str(e)
                },
                'status_http':e.args[1] if len(e.args) > 1 else 404
            }
            
        return response
    
    
    @classmethod
    def getGeneratedCode(cls, data):
        try:
            typeD = data["type"]
            data.pop("type")
            
            if len(data) == 0:
                raise Exception("Usuario no encontrado.", 400)
            
            searchUser = UserClass.getData(**data)

            if len(searchUser) == 0:
                raise Exception("Usuario no encontrado.", 400)
            
            user = UserClass.getDataFirst(searchUser[0]["id"])

            if "id" not in user:
                raise Exception("El usuario no existe.")
            
            #* Se genera codigo temporal
            dataCode = {
                "type":typeD,
                "user_id":user["id"],
                "code":random.randint(100000, 999999),
                "status_id": Code("AVAILABLE")
            }
            
            resulCode = TempCodeClass.postData(**dataCode)
            if("id" not in resulCode):
                raise Exception("No se creo el codigo temporal")
            
            listCodeSendEmail = [
                "RecoverPasswordByEmail",
                "verifyEmail",
                "RecoverUserByEmail",
                "ChangePasswordByEmail",
            ]
            
            #* Se envia el codigo al email si esta en la lista de email
            if(typeD in listCodeSendEmail):
                # if typeD != "verifyEmail" and user["verified_email"] != 1:
                    # raise Exception("El email debe estar verificado")
                
                name = user["username"] if user["fullname"] is None else user["fullname"]
                
                email = send(resulCode["code"], user["email"], name, typeD)
                if(email["status_http"] == 200):
                    resulCode.pop("code")
                else:
                    raise Exception(email["response"]["message"])
            response = {
                "response":resulCode,
                "status_http": 200
            }
        except Exception as e:
            response = {
                'response':{
                    'message'  : e.args[0] if len(e.args) > 0 else str(e)
                },
                'status_http':e.args[1] if len(e.args) > 1 else 404
            }
        
        return response
    
    @classmethod
    def deleteUser(cls, data):
        try:
            user_logged = verifyToken()["response"]["user_id"]
            user = UserClass.getDataFirstPut(user_logged)
            if user is not None:
                verificBot = UserClass.getDataFirst(user_logged)
                if verificBot["company"] is not None:
                    company = CompanyClass.getDataFirstPut(verificBot["company"]["id"])
                
                if verificBot["bots"] is not None:
                    bot = BootsClass.getDataFirst(verificBot["bots"]["name"])
                
                response = UserClass.deletData(user)
                if "message" in response:
                    response = {
                        "response"    : response, 
                        "status_http" : 200
                    }
                    
                    if verificBot["company"] is not None:
                        deleteCompany = CompanyClass.deletData(company)
                    
                    if verificBot["bots"] is not None:
                        deleteBot = BootsClass.deletData(bot)
                else:
                    raise Exception("Ocurrio un error al eliminar la cuenta.", 500)
            else:
               raise Exception("usuario no encontrado.", 404)
        except Exception as e:
            response = {
                'response':{
                    'message'  : e.args[0] if len(e.args) > 0 else str(e)
                },
                
                'status_http':e.args[1] if len(e.args) > 1 else 404
            }
            
        return response