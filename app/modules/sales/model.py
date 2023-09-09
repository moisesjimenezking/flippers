from .classStructure import SalesClass
from flask import jsonify
from modules.orders.model import Orders
from modules.bots.model import Bots
from modules.product.model import Product
from modules.delivery.model import Delivery
from modules.chatters.model import Chatters
from .statusCodes import Code
from datetime import datetime, timedelta
from library.VerifyToken import verifyToken
import logging, json, requests, re

logging.basicConfig(level=logging.DEBUG)

class Sales:
    
    @classmethod
    def getChattersData(cls, data):
        try:
            user_logged = verifyToken()["response"]["user_id"]
            salesSearch = dict()
            salesSearch.update({"user_id": user_logged})
            chatters = Chatters.getData(data)
            if chatters["status_http"] == 200:
                chatters = chatters["response"]
                for x in range(len(chatters)):
                    chatters[x]["name"] = "Desconocido" if chatters[x]["name"] is None else chatters[x]["name"]
                    chatters[x].update({"billing":{"currency_int":"Bs.0.00","currency_ext":"$0.00"}})
                    
                    # salesSearch.update({"user_id": user_logged})
                    # chatters[x].update({"sales":})
                response = {"response":chatters, "status_http": 200}
            else:
                raise Exception("Sin datos", 404)
        except Exception as e:
            response = {
                "response":{
                    "message":e.args[0] if len(e.args) > 0 else str(e)
                }, 
                "status_http": 404
            }
        
        return response

    @classmethod
    def getSalesData(cls, data):
        try:
            #* Se extraen las ventas del usuario loggeado
            user_logged = verifyToken()["response"]["user_id"]
            data.update({"user_id": user_logged})

            #* Si el parametro status es enviado se convierte y extrae por su valor de DB correcto
            if "status" in data:
                status = Code(data["status"])
                data.pop("status")
                data.update({"status_id": status})
                
            # elif "status_id" in data and data:
            #     data.update({"status_id": Code(data["status"])})
                
            response = SalesClass.getData(**data)
            
            if(len(response) == 0):
                raise Exception("Sin datos", 404)
            else:
                response = {"response":response, "status_http": 200}
                
        except Exception as e:
            response = {
                'response':{
                    'message' : e.args[0] if len(e.args) > 0 else str(e)
                },
                'status_http':e.args[1] if len(e.args) > 1 else 404
            }
        
        return response

    @classmethod
    def postSalesData(cls, data):
        try:
            #* Se extraen las ventas del usuario loggeado
            user_logged = verifyToken()["response"]["user_id"]
            
            #* Se extrae el bot del user logeado
            bot = Bots.getBootsData({"user_id":user_logged})
            if bot["status_http"] != 200:
                raise Exception("El bot no fue encontrado.")
            
            #* Se confirma la existencia y pertenecia del producto
            product = Product.getProduct({"bot_id":bot["response"][0]["id"], "id":data["product_id"]})
            if product["status_http"] != 200:
                raise Exception("El producto no fue encontrado.")
            
            #* Se crea la orden
            order = Orders.postData({})
            if order["status_http"] != 201:
                raise Exception("Lo sentimos hubo un error al crear la orden de compra.", 400)
            
            #? Se crea el chatters si no existe
            dataChatters = {"user_id":user_logged, "chatter_phone":data["phone_chatters"]}
            Chatters.getVerifiData(dataChatters)

            data.update({
                "user_id"       : user_logged,
                "bot_id"        : bot["response"][0]["id"],
                "orders_id"     : order["response"][0]["id"],
                "price"         : product["response"][0]["price"],
                "currency_code" : product["response"][0]["currency_code"],
            })
            
            response = SalesClass.postData(**data)
            if "id" in response: 
                response = {
                    "response"      : response, 
                    "status_http"   : 201
                }
            else:
                raise Exception("Fallo al crear la compra.",404)
            
        except Exception as e:
            response = {
                'response':{
                    'message'  : e.args[0] if len(e.args) > 0 else str(e)
                },
                
                'status_http':e.args[1] if len(e.args) > 1 else 404
            }
            
        return response
    
    @classmethod
    def postBotData(cls, data):
        try:
            logging.debug(str(data))            
            #* Se confirma la existencia del bot
            bot = Bots.getBootsData({"name":data["bot_name"]})
            if bot["status_http"] == 200:
                bot = bot["response"][0]
            else:
                raise Exception("El bot no fue encontrado.")

            if len(data["products"]) == 0:
                if data["code"].upper() == "DELIVERY":
                    delivery = Delivery.postData({"direction":data["location"], "phone_chatters":data["chatter_phone"], "bot_name":data["bot_name"]})
                    if delivery["status_http"] == 201:
                        return{
                            "response"    : {
                                "message" : "📢 Te informo que he actualizado tu dirección. Así que, la próxima vez que hagas una compra, ¡nuestros asesores la enviaran a tu dirección actual! 🏡🚚✨", 
                                "details" : list(), 
                                "error"   : None,
                                "note"    : None
                            },
                            "status_http" : 201
                        }
                    else:
                        raise Exception("Lo sentimos hubo un error al crear el registro del delivery.", 400)
                else:
                    raise Exception("Para generar una compra es nesesario que nos indique el nombre del producton")
                
            #* Se confirma la existencia y pertenecia del producto
            product = Product.getProductSales({"bot_id":bot["id"], "name":data["products"][0]})
            if product["status_http"] == 200:
                product = product["response"][0]
            else:
                returned = False
                response = Product.getProductBotPrice({"bot_name":bot["name"], "products":data["products"][0]})
                if len(response["response"]["details"]) == 1:
                    name = response["response"]["details"][0]["message"].split("*")[1]
                    product = Product.getProductSales({"bot_id":bot["id"], "name":name})
                    if product["status_http"] == 200:
                        product = product["response"][0]
                    else:
                        raise Exception("El producto no fue encontrado.")
                elif len(response["response"]["details"]) > 1:
                    response["response"]["message"] = "¡Hey! Parece que estás buscando algo genial.\n\nPermíteme mostrarte los productos que coinciden con tu compra. Pero antes, necesito que me indiques de manera detallada el nombre de tu producto. ¡Estoy emocionado por ayudarte a encontrar lo que necesitas!"
                    returned = True
                else:
                    raise Exception("El producto no fue encontrado.")
            
                if returned:
                    return response
            dataOrder = {}
            
            #* Si el code es delivery se comprueba que venga el campo direction
            if data["code"].upper() == "DELIVERY":
                if "location" in data and data["location"] is not None:
                    delivery = Delivery.postData({"direction":data["location"], "phone_chatters":data["chatter_phone"], "bot_name":data["bot_name"]})
                    if delivery["status_http"] == 201:
                        delivery = delivery["response"][0]
                        dataOrder.update({"delivery_id":delivery["id"]})
                    else:
                        raise Exception("Lo sentimos hubo un error al crear el registro del delivery.", 400)
                else:
                    raise Exception("Por favor envíe una dirección para su delivery.", 400)
            
            quantiy = data["quantity"] if "quantity" in data and isinstance(data["quantity"], int) and data["quantity"] >= 1 else 1
            while quantiy > 0:
                verificSalesPending = SalesClass.getData(**{"phone_chatters":data["chatter_phone"], "status_id":Code("PENDING")})
                if verificSalesPending is not None and len(verificSalesPending) > 0:
                    response = Orders.putDataAdd({
                        "id":verificSalesPending[0]["orders_id"],
                        "product_add_json":{
                            "id"            : str(product["id"]),
                            "amount"        : str(product["price"]),
                            "currency_code" : str(product["currency_code"])
                        }
                    })
                    
                    if response["status_http"] == 200:
                        response = response["response"]
                else:
                    #* Se crea la orden
                    order = Orders.postData(dataOrder)
                    if order["status_http"] == 201:
                        order = order["response"][0]
                    else:
                        raise Exception("Lo sentimos hubo un error al crear la orden de compra.", 400)
                    
                    dataSales = {
                        "user_id"       : bot["user_id"],
                        "bot_id"        : bot["id"],
                        "orders_id"     : order["id"],
                        "product_id"    : product["id"],
                        "price"         : product["price"],
                        "currency_code" : product["currency_code"],
                        "phone_chatters": re.sub(r"[^0-9]", "", data["chatter_phone"]),
                    }
                        
                    response = SalesClass.postData(**dataSales)

                quantiy -= 1
                
            if 'id' in response:
                messaAux = ""
                if product["description"] is not None:
                    messaAux = product["description"]+"\n\n"
                    
                if product["discount"] is not None:
                    auxDiscount = round(float(product["price"]) - ((float(product["price"]) * float(product["discount"]))/100), 2)
                    product["currency_code"] = "Bs. " if product["currency_code"] == "Bs" else product["currency_code"]
                    product["price"] = "{}{}".format(product["currency_code"], auxDiscount)
                    
                    
                response["note"] = "El monto total a pagar por su compra es de *{}*. \nPronto nos pondremos en contacto para concretar su comprar. ¡Gracias por su compra!".format(product["price"])
                response["message"] = messaAux+"✅📋```Su compra esta en proceso pronto lo contactaremos.```" if data["code"].upper() != "DELIVERY" else "✅🛵```Pronto lo contactaremos para concretar la entrega.```"
            else:
                raise Exception("Ocurrio un error al registrar la compra.")
            
            response = {
                "response"    : {
                    "message" : response["message"], 
                    "details" : list(), 
                    "error"   : None,
                    "note"    : response["note"] if "note" in response else None
                },
                "status_http" : 201
            }
        except Exception as e:
            response = {
                'response':{
                    "note": None,
                    'message': None,
                    'error' : e.args[0] if len(e.args) > 0 else str(e),
                    'details' : list()
                },
                
                'status_http':e.args[1] if len(e.args) > 1 else 404
            }
            
        return response
    
    @classmethod
    def getTimeData(cls, data):
        try:
            #* Se extraen las ventas del usuario loggeado
            user_logged = verifyToken()["response"]["user_id"]
            
            #* listDay
            listDay = {
                "Monday":"Lunes", 
                "Tuesday":"Martes",
                "Wednesday":"Miércoles",
                "Thursday":"Jueves",
                "Friday":"Viernes",
                "Saturday":"sábado",
                "Sunday":"domingo"
            }
            
            #* Se crean valores temporales para el filtro
            datetimeNow = datetime.now()
            daysAux = 8
            response = list()
            for x in range(daysAux):
                if daysAux == 1:
                    break
                
                datetimeAux = datetimeNow - timedelta(days=daysAux)
                datetimeEnd = datetimeAux.strftime('%Y-%m-%d')+' 23:59:59'
                datetimeStart = datetimeAux.strftime('%Y-%m-%d')+' 00:00:00'
                nameDay = listDay[datetimeAux.strftime('%A')]
                
                resultDay = SalesClass.getDataTime(user_logged, datetimeEnd, datetimeStart)

                objecAux = {
                    "day"           : nameDay,
                    "quantity_sale" : 0,
                    "billing"       : {"currency_int":0, "currency_ext":0},
                    "expected_sale" : 10
                }
                
                if len(resultDay) > 0:
                    objecAux["quantity_sale"] = len(resultDay)
                    for dayResult in range(len(resultDay)):
                        if resultDay[dayResult]["order"]["product_add_json"] is not None:
                            objecAux["quantity_sale"] = objecAux["quantity_sale"] + len(resultDay[dayResult]["order"]["product_add_json"])
                            jsonAux = resultDay[dayResult]["order"]["product_add_json"]
                            for json in range(len(jsonAux)):
                                jsonCurrencyAux = jsonAux[json]["currency_code"]
                                jsonAmountAux = jsonAux[json]["amount"]
                                
                                if jsonCurrencyAux == "Bs":
                                    objecAux["billing"]["currency_int"] = float(objecAux["billing"]["currency_int"])+float(jsonAmountAux)
                                    
                                if jsonCurrencyAux == "$":
                                    objecAux["billing"]["currency_ext"] = float(objecAux["billing"]["currency_ext"])+float(jsonAmountAux)

                                
                        if resultDay[dayResult]["currency_code"] == "Bs":
                            objecAux["billing"]["currency_int"] = float(objecAux["billing"]["currency_int"])+float(resultDay[dayResult]["price"])
                            
                        if resultDay[dayResult]["currency_code"] == "$":
                            objecAux["billing"]["currency_ext"] = float(objecAux["billing"]["currency_ext"])+float(resultDay[dayResult]["price"])

                    objecAux["billing"]["currency_ext"] = "$ "+str(objecAux["billing"]["currency_ext"])
                    objecAux["billing"]["currency_int"] = "Bs "+str(objecAux["billing"]["currency_int"])
                    
                response.append(objecAux)
                daysAux -= 1

            if(len(response) == 0):
                raise Exception("Sin datos",404)

            response = {
                "response":response, 
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
    def putSalesData(cls, data):
        try:
            #* Se extraen las ventas del usuario loggeado
            user_logged = verifyToken()["response"]["user_id"]
            
            #* Se extrae la venta
            sales = SalesClass.getDataFirst(data["id"])
            if "id" not in sales:
                raise Exception("Venta no encontrada")

            if sales["status_id"] == "CANCELLED":
                raise Exception("Esta venta fue cancelada")
            
            #* direccion
            if "direction" in data:
                order = Orders.getData({"id":sales["orders_id"]})
                if order["status_http"] != 200:
                    raise Exception("Orden no encontrada")
                
                if order["response"][0]["delivery_id"] is None:
                    delivery = Delivery.postData({"direction":data["direction"], "phone_chatters":sales["phone_chatters"], "bot_id":sales["bot_id"]})
                    if delivery["status_http"] != 201:
                        raise Exception(delivery["response"]["message"], delivery["status_http"])
                    
                    order = Orders.putData({"id":order["response"][0]["id"], "delivery_id":delivery["response"][0]["id"]})
                else:
                    delivery = Delivery.putData({"id":order["response"][0]["delivery_id"], "direction":data["direction"]})
                    if delivery["status_http"] != 201:
                        raise Exception(delivery["response"]["message"], delivery["status_http"])
                    
            #* agregar producto
            if "product_id" in data:
                #* Se extrae el bot del user logeado
                bot = Bots.getBootsData({"user_id":user_logged})
                if bot["status_http"] != 200:
                    raise Exception("El bot no fue encontrado.")
            
                #* Se confirma la existencia y pertenecia del producto
                product = Product.getProduct({"bot_id":bot["response"][0]["id"], "id":data["product_id"]})
                logging.debug(product)
                if product["status_http"] != 200:
                    raise Exception("El producto no fue encontrado.")
            
                orders = Orders.putDataAdd({
                    "id":sales["orders_id"],
                    "product_add_json":{
                        "id"            : str(product["response"][0]["id"]),
                        "amount"        : str(product["response"][0]["price"]),
                        "currency_code" : str(product["response"][0]["currency_code"])
                    }
                })
                
            #* Cambio de status
            if "status_id" in data or "status" in data:
                status = data["status_id"] if "status_id" in data else data["status"]
                if status != sales["status_id"]:
                    sales = SalesClass.getDataFirstPut(data["id"])
                    sales.status_id = Code(status)
                    
                    update = SalesClass.putData(sales)
                    if "id" not in update:
                        raise Exception("Ocurrio un error al intentar actualizar el producto.")
                    
                    try:
                        if status == "SOLD":
                            bot = Bots.getBootsData({"user_id":update["user_id"]})
                            logging.debug(str(bot))
                            url = "https://f848-2a09-bac5-d3a5-aa-00-11-169.ngrok-free.app/api/v1/assistant/{}/send-califications-poll".format(bot["response"][0]["name"])
                            payload = json.dumps({
                                "phone": update["phone_chatters"]
                            })
                            headers = {
                            'Content-Type': 'application/json'
                            }
                            result = requests.request("POST", url, headers=headers, data=payload)
                            logging.debug(result)
                    except:
                        pass
                    
                    response = {
                        "response" : update,
                        "status_http": 201
                    }
                else:
                    raise Exception("Sin cambios", 304)
            else:
                if len(data) <= 1:
                    raise Exception("Sin cambios", 304)
                else:
                    sales = SalesClass.getDataFirst(data["id"]) 
                    response = {
                        "response" : sales,
                        "status_http": 201
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
    def getSalesDataChatters(cls, data):
        try:
            response = SalesClass.postData(**data)
            if "id" in response: 
                response = {
                    "response"      : response, 
                    "status_http"   : 201
                }
            else:
                raise Exception("Fallo al crear la compra.",404)
            
        except Exception as e:
            response = {
                'response':{
                    'message'  : e.args[0] if len(e.args) > 0 else str(e)
                },
                
                'status_http':e.args[1] if len(e.args) > 1 else 404
            }
            
        return response
    