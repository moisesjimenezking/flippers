from . import classStructure
from library.boto import boto
from modules.bots.model import Bots
from modules.bots.classStructure import BootsClass
from modules.chatters.model import Chatters
from modules.company.classStructure import CompanyClass
import logging, re
from library.VerifyToken import verifyToken
from .statusCodes import Code


logging.basicConfig(level=logging.DEBUG)
ProductClass = classStructure.ProductClass

class Product:
    
    @classmethod
    def getProduct(cls, data):
        try:
            user_logged = verifyToken()["response"]["user_id"]
            
            #* si es enviado el user_id
            if('user_id' in data):
                search = {"user_id": data['user_id']}
            else:
                search = {"user_id": user_logged}
                
            #* si es enviado el bot_id
            if 'bot_id' in data:
                if "search" in locals():
                    search.update({'bot_id': data['bot_id']})
                else:
                    search = {'bot_id': data['bot_id']}

            if 'name' in data:
                search.update({'name': data['name']})
                
            if 'id' in data:
                search.update({'id': data['id']})

            if 'status_id' not in data:
                search.update({'status_id':Code("AVAILABLE")})
                
            response = ProductClass.getData(**search)
            if(len(response) == 0):
                raise Exception("Sin datos.", 404)
            else:
                response = {"response":response, "status_http": 200}
        except Exception as e:
            response = {
                'response':{
                    'message': 'Se produjo un error',
                    'error'  : e.args[0] if len(e.args) > 0 else str(e)
                },
                
                'status_http':e.args[1] if len(e.args) > 1 else 404
            }
        
        return response
    
    @classmethod
    def getProductSales(cls, data):
        try:
            if 'status_id' not in data:
                data.update({'status_id':Code("AVAILABLE")})
                
            response = ProductClass.getData(**data)
            if(len(response) == 0):
                raise Exception("Sin datos.", 404)
            else:
                response = {"response":response, "status_http": 200}
        except Exception as e:
            response = {
                'response':{
                    'message': 'Se produjo un error',
                    'error'  : e.args[0] if len(e.args) > 0 else str(e)
                },
                
                'status_http':e.args[1] if len(e.args) > 1 else 404
            }
        
        return response
    
    @classmethod
    def postData(cls, data):
        try:
            user_logged = verifyToken()["response"]["user_id"]
            
            if "base64" in data:
                bot = BootsClass.getDataFirstUser(user_logged)
                if "name" not in bot:
                    raise Exception("Bot no encontrado.")
                
                product_name = re.sub(r"[^\w\s]", "", data["name"]).replace(" ", "_")+"."+data["base64"].split("/")[1].split(";")[0]
                base64 = data["base64"].split(",")[-1]
                content_type = data["base64"].split(":")[1].split(";")[0]
                url = boto(bot["name"], product_name, base64, content_type)

                if url["status_http"] == 200:
                    data.update({"url":url["response"]["url"],"user_id":user_logged,"bot_id":bot["id"]})
                    data.pop("base64")
                else:
                    raise Exception("error url", 500)
                
            response = ProductClass.postData(**data)
            response = {"response":response, "status_http": 404 if 'message' in response else 201}
        except Exception as e:
            response = {
                'response':{
                    'message': 'Se produjo un error',
                    'error'  : e.args[0] if len(e.args) > 0 else str(e)
                },
                
                'status_http':e.args[1] if len(e.args) > 1 else 404
            }
            
        return response
    
    @classmethod
    def putData(cls, data):
        try:
            user_logged = verifyToken()["response"]["user_id"]
            product = ProductClass.getDataFirst(data.get("id"))
                
            if product is not None:
                if product.user_id != user_logged:
                    raise Exception("La ID de este producto no le pertenece al usuario.", 400)
                
                if "base64" in data:
                    bot = BootsClass.getDataFirstUser(user_logged)
                    if "name" not in bot:
                        raise Exception("Bot no encontrado.")
                    
                    product_name = re.sub(r"[^\w\s]", "", data["name"]).replace(" ", "_")+"."+data["base64"].split("/")[1].split(";")[0]
                    base64 = data["base64"].split(",")[-1]
                    content_type = data["base64"].split(":")[1].split(";")[0]
                    url = boto(bot["name"], product_name, base64, content_type)

                    if url["status_http"] == 200:
                        data.update({"url":url["response"]["url"],"user_id":user_logged,"bot_id":bot["id"]})
                        data.pop("base64")
                    else:
                        raise Exception("error url", 500)
                
                change = False
                
                for key, value in data.items():
                    if hasattr(product, key): 
                        attr = getattr(product, key)
                        if str(attr) != str(value):
                            change =True
                            setattr(product, key, value)

                if(change):
                    response = ProductClass.putData(product)
                    if "message" in response:
                        raise Exception(response["message"], 400)
                    
                    response = {
                        "response"    : response, 
                        "status_http" : 201
                    }
                else:
                    raise Exception("Sin cambios.", 304)
            else:
               raise Exception("Producto no encontrado.", 404)
        except Exception as e:
            response = {
                'response':{
                    'message'  : e.args[0] if len(e.args) > 0 else str(e)
                },
                
                'status_http':e.args[1] if len(e.args) > 1 else 404
            }
            
        return response
    
    @classmethod
    def getProductBot(cls, data):
        try:
            if 'bot_name' in data:
                bot = BootsClass.getDataFirst(data["bot_name"])
                if bot is None:
                    raise Exception("Bot no encontrado")
                else:
                    data.pop("bot_name")
                    data.update({"bot_id":bot.id})
            else:#
                raise Exception("Bot no encontrado")
            
            company = CompanyClass.getDataFirstUser(bot.user_id)
            
            #* Se consultan los productos del bot
            products = cls.getProduct({"bot_id":bot.id})
            if(products["status_http"] != 200):
                messageError = "Estimado usuario\n\nGracias por su interés en nuestros productos. Le aseguramos que enviaremos nuestro catálogo lo antes posible."
                messageError = messageError+"\n\n*{}*".format(company["company_name"]) if "company_name" in company else messageError
                raise Exception(messageError)
            else:
                products = products["response"]
                
            message = ""
            for product in products:
                if product["discount"] is not None:
                    auxDiscount = round(float(product["price"]) - ((float(product["price"]) * float(product["discount"]))/100), 2)
                    product["currency_code"] = "Bs. " if product["currency_code"] == "Bs" else product["currency_code"]
                    product["price"] = "~{}{}~ 👉 {}{}".format(product["currency_code"], float(product["price"]), product["currency_code"], auxDiscount)
                    
                message = message+"*{}*\nPrecio: *{}*\n\n{}\n\n__{}__".format(
                    product["name"],
                    product["price"],
                    product["description"],
                    product["footer"]
                )
            
            response = {
                "response":{"message":message},
                "status_http":200
            }                
        except Exception as e:
            response = {
                'response':{
                    'message': None,
                    'error' : e.args[0] if len(e.args) > 0 else str(e),
                    'details' : list()
                },
                
                'status_http':e.args[1] if len(e.args) > 1 else 404
            }
        
        return response
    
    @classmethod
    def getProductBotPrice(cls, data):
        try:
            if 'bot_name' in data:
                bot = BootsClass.getDataFirst(data["bot_name"])
                if bot is None:
                    raise Exception("Bot no encontrado")
            else:
                raise Exception("Bot no encontrado")
            
            message = ""
            note = ""
            details = list()
            notProduct = True
            if "products" in data:
                if type(data["products"]) == str:
                    try:
                        data["products"] = eval(data["products"])
                    except:
                        data["products"] = [data["products"]]
                        
                if len(data["products"]) > 0:
                    notProduct = False
                    search = True
                    for product in data['products']:
                        if search:
                            productsSearch = ProductClass.getElastic(bot.id, product)

                            if len(productsSearch) > 0:
                                for productUnic in productsSearch:
                                    if productUnic["discount"] is not None:
                                        auxDiscount = 0 if float(productUnic["discount"]) == 0 else round(float(productUnic["price"]) - ((float(productUnic["price"]) * float(productUnic["discount"]))/100), 2)
                                        if auxDiscount == 0:
                                            productUnic["price"] = "{} {}".format(productUnic["currency_code"], float(productUnic["price"]))
                                        else:
                                            productUnic["price"] = "~{} {}~ 👉 {} {}".format(productUnic["currency_code"], float(productUnic["price"]), productUnic["currency_code"], auxDiscount)
                                        
                                    if len(productsSearch) <= 3:
                                        messageAux = "*{}*\nPrecio: *{}*\n\n{}\n\n_{}_".format(
                                            productUnic["name"],
                                            productUnic["price"],
                                            productUnic["description"],
                                            productUnic["footer"]
                                        )
                                        auxObject = {"message":messageAux, "url":productUnic["url"]}
                                        details.append(auxObject)
                                    else:
                                        messageAux = "*{}*\nPrecio: *{}*".format(
                                            productUnic["name"],
                                            productUnic["price"],
                                        )
                                                                
                                        message = message+messageAux+"\n\n"
                                        
                                search = False
                                
                                if len(productsSearch) > 3:
                                    ej = "*Ej: Detalles {}*".format(productUnic["name"])    
                                    message = message+"Si quieres más detalles sobre un producto, simplemente envíame un mensaje con la palabra *DETALLES* seguida del nombre del producto.\n\n"+ej.upper()
                                else:
                                    ej = "*Ej: Comprar {}*".format(productUnic["name"])
                                    note = "Si deseas adquirir un producto, simplemente envía un mensaje con la palabra *COMPRAR* seguida del nombre del producto que deseas adquirir.\n\n"+ej.upper()
                            else:
                                search = True
                        else:
                            break
            
            if notProduct:
                message = ""
                productsSearch = ProductClass.getData(**{"bot_id": bot.id})
                if len(productsSearch) > 0:
                    for productUnic in productsSearch:
                        if productUnic["discount"] is not None:
                            auxDiscount = 0 if float(productUnic["discount"]) == 0 else round(float(productUnic["price"]) - ((float(productUnic["price"]) * float(productUnic["discount"]))/100), 2)
                            if auxDiscount == 0:
                                productUnic["price"] = "{} {}".format(productUnic["currency_code"], float(productUnic["price"]))
                            else:
                                productUnic["price"] = "~{} {}~ 👉 {} {}".format(productUnic["currency_code"], float(productUnic["price"]), productUnic["currency_code"], auxDiscount)
                                        
                            # auxDiscount = round(float(productUnic["price"]) - ((float(productUnic["price"]) * float(productUnic["discount"]))/100), 2)
                            # productUnic["price"] = "~{} {}~ 👉 {} {}".format(productUnic["currency_code"], float(productUnic["price"]), productUnic["currency_code"], auxDiscount)
                            
                        if len(productsSearch) <= 3:
                            messageAux = "*{}*\nPrecio: *{}*\n\n{}\n\n_{}_".format(
                                productUnic["name"],
                                productUnic["price"],
                                productUnic["description"],
                                productUnic["footer"]
                            )
                            auxObject = {"message":messageAux, "url":productUnic["url"]}
                            details.append(auxObject)
                        else:
                            messageAux = "*{}*\nPrecio: *{}*".format(
                                productUnic["name"],
                                productUnic["price"],
                            )
                                                    
                            message = message+messageAux+"\n\n"
                    
                    if len(productsSearch) > 3:
                        ej = "*Ej: Detalles {}*".format(productUnic["name"])
                        note = "Si quieres más detalles sobre un producto, simplemente envíame un mensaje con la palabra *DETALLES* seguida del nombre del producto.\n\n"
                    else:
                        ej = "*Ej: Comprar {}*".format(productUnic["name"])
                        note = "Si deseas adquirir un producto, simplemente envía un mensaje con la palabra *COMPRAR* seguida del nombre del producto que deseas adquirir.\n\n"

            if len(details) == 0 and len(productsSearch) > 0:
                response = {
                    "response":{
                        "message":message,
                        "details":list(),
                        "note": note,
                        "error": None
                    },
                    "status_http":200
                }
            elif len(details) > 0:
                response = {
                    "response":{
                        "message":"Por favor, indícame si alguno de los siguientes productos es el que estás preguntando 📋🔍" if len(details) > 1 else None,
                        "details":details,
                        "note": note,
                        "error": None
                    },
                    "status_http":200
                }
            else:
                response = {
                    "response":{
                        "message":"No hay productos disponibles en este momento.",
                        "details":list(),
                        "note": None,
                        "error": None
                    },
                    "status_http":200
                }
                
        except Exception as e:
            response = {
                'response':{
                    'message': None,
                    'error' : e.args[0] if len(e.args) > 0 else str(e),
                    'details' : list(),
                    "error": None
                },
                
                'status_http':e.args[1] if len(e.args) > 1 else 404
            }
        
        return response
    
    @classmethod
    def getProductLike(cls, data):
        try:
            #* si es enviado el bot_id
            if 'bot_id' not in data:
                raise Exception("Nombre de producto requerido")

            if 'name' not in data:
                raise Exception("Nombre de producto requerido")

            response = ProductClass.getElastic(data['bot_id'], data['name'])
            if(len(response) == 0):
                raise Exception("Sin datos.", 404)
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
    def deletData(cls, data):
        try:
            user_logged = verifyToken()["response"]["user_id"]
            product = ProductClass.getDataFirst(data.get("id"))
            if product is not None:
                if product.user_id != user_logged:
                    raise Exception("La ID de este producto no le pertenece al usuario.", 400)
                else:
                    
                    response = ProductClass.deletData(product)
                    if "message" in response:
                        response = {
                            "response"    : response, 
                            "status_http" : 200
                        }
                    else:
                        raise Exception("Ocurrio un error al eliminar el producto.", 500)
            else:
               raise Exception("Producto no encontrado.", 404)
           
        except Exception as e:
            response = {
                'response':{
                    'message'  : e.args[0] if len(e.args) > 0 else str(e)
                },
                
                'status_http':e.args[1] if len(e.args) > 1 else 404
            }
            
        return response