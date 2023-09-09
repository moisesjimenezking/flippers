from . import classStructure
from library.Email import sendEmail
import logging

logging.basicConfig(level=logging.DEBUG)

OrdersClass = classStructure.OrdersClass

class Orders:
    
    @classmethod
    def getData(cls, data):
        try:
            response = OrdersClass.getData(**data)
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
            response = OrdersClass.postData(**data)
            response = {"response":response, "status_http": 404 if 'message' in response else 201}
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
            orders = OrdersClass.getDataFirstPut(data.get("id"))
            change = False
            
            for key, value in data.items():
                if hasattr(orders, key): 
                    attr = getattr(orders, key)
                    if str(attr) != str(value):
                        change =True
                        setattr(orders, key, value)

            if(change):
                response = OrdersClass.putData(orders)
                response = {"response":response, "status_http": 404 if 'message' in response else 201}
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
    def putDataAdd(cls, data):
        try:
            orders = OrdersClass.getDataFirstPut(data.get("id"))

            if orders.product_add_json is None:
                listOrders = [data["product_add_json"]]
            else:
                listOrders = orders.product_add_json 
                listOrders.append(data["product_add_json"])
            
            #* Se limpia la orden primero
            setattr(orders, "product_add_json", None)
            response = OrdersClass.putData(orders)
            
            #* Se asigna el nuevo producto a la orden
            setattr(orders, "product_add_json", listOrders)
            response = OrdersClass.putData(orders)
            
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