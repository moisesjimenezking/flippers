# from . import formValidation
from library.VerifyToken import verifyToken

class ParamValidation:

    #* Función que contiene las reglas de parámetros para el Get de user
    def chattersList(cls):
        param = {
            'required':{
                "chatter_phone",
                "bot_name"
            },
            'optional':{
                "chatter_name",
                "profile_img"        
            },
        }
        
        return param
    
    #* Función que contiene las reglas de parámetros para el Post de user
    def productPostRute(cls):
        param = {
            'required':set(),
            'optional':set(),
        }
        
        return param
    
    #* Función que contiene las reglas de parámetros para el Put de user
    def productPutRute(cls):
        param = {
            'required':set(),
            'optional':set(),
        }
        
        return param
    
    #* Función que contiene las reglas de parámetros para el Deleted de product
    def productDeletedRute(cls):
        param = {
            'required':set(),
            'optional':set(),
        }
        
        return param
    
    
    @classmethod
    def ValidationParam(cls, data, rute):
        try:
            #* respuesta por defecto en caso de no ocurrir ningún error
            response = {
                'response'   : {"message":True},
                'status_http': 200
            }
            
            #* Lista de funciones que contienen las reglas de parámetros
            listFuntion = {
                '/getchattersList' : 'chattersList',
            }
            
            #* Lista de métodos que requieren token
            requiredToken = {
                '/getChatters',
            }
            
            #* Si el método requiere token se verifica el estado del token
            if(rute in requiredToken):
                token = verifyToken()
                if(token["status_http"] != 200):
                    raise Exception(token["response"]["message"])
        
            #* Sé la ruta está en la lista se verifican los parámetros enviados
            if(rute in listFuntion):
                method = getattr(ParamValidation, listFuntion[rute])
                params = method(cls)
                
                #* Si el método tiene parámetros requeridos, se verifica la resección de estos
                if(bool(params['required'])):
                    for key in params['required']:
                        if(key not in data):
                            key = "password" if key == "passwd" else key
                            raise Exception(key+" es un parámetro requerido")

                #* Se unen data set de parametros opcionales y requeridos
                setMerge = params["required"].union(params['optional']) 
                    
                #* Lista de elementos a descartar
                listDel = list()
                
                #* Sí hay parámetros en la data se evalúan que estén requeridos u opcionales
                if(bool(data)):
                    for key in data:
                        if data[key] is not None and len(data[key]) == 0:
                            listDel.append(key)
                            
                        if(key not in setMerge):
                            key = "password" if key == "passwd" else key
                            raise Exception(key+" es un parámetro no permitido")
                
                if len(listDel) > 0:
                    for key in listDel:
                        data.pop(key)     
                        
                #* si hay parámetros en la data se evalúa que cumpla con los formularios
                # if bool(data):
                #     validationForm = formValidation.FormValidation(data, rute)
                #     if(validationForm["status_http"] != 200):
                #         raise Exception(validationForm["response"]["message"])

        except Exception as e:
            response = {
                'response'   : {"message":str(e)},
                'status_http': 400
            }
            
        return response