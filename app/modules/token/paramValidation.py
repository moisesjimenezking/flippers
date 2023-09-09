from .  import formValidation
from library.VerifyToken import verifyToken


class ParamValidation:

    #* Reglas de parametros para el Get de token
    def tokenGetRute(cls):
        param = {
            'required':set(),
            'optional':{
                'username'
                'user_id'
            }
        }
        
        return param
    
    #* Reglas de parametros para el POST de token
    def tokenPostRute(cls):
        param = {
            'required':{
                'username',
                'passwd'
            },
            'optional':set(),
        }
        
        return param
    
    @classmethod
    def ValidationParam(cls, data, rute):
        try:
            #* respuesta por defecto True
            response = {
                'response'   : {"message":True},
                'status_http': 200
            }
            
            listFuntion = {
                '/getToken'   : 'tokenGetRute',
                '/postToken' : 'tokenPostRute',
            }
            
            #* Lista de métodos que requieren token
            requiredToken = {
                '/getToken',
            }
            
            #* Si el método requiere token se verifica el estado del token
            if(rute in requiredToken):
                token = verifyToken()
                if(token["status_http"] != 200):
                    raise Exception(token["response"]["message"])
                
            if(rute in listFuntion):
                method = getattr(ParamValidation, listFuntion[rute])
                params = method(cls)

                if(bool(params['required'])):
                    for key in params['required']:
                        if(key not in data):
                            key = "password" if key == "passwd" else key
                            raise Exception(key+" es un parametro requerido")

                setMerge = params["required"].union(params['optional']) 
                
                #* Lista de elementos a descartar
                listDel = list()
                   
                if(bool(data)):
                    for key in data:
                        if data[key] is not None and len(data[key]) == 0:
                            listDel.append(key)
                            
                        if(key not in setMerge):
                            key = "password" if key == "passwd" else key
                            raise Exception(key+" es un parametro no permitido")
                       
                if len(listDel) > 0:
                    for key in listDel:
                        data.pop(key) 
                         
                if bool(data):
                    validationForm = formValidation.FormValidation(data, rute)
                    if(validationForm["status_http"] != 200):
                        raise Exception(validationForm["response"]["message"])

        except Exception as e:
            response = {
                'response'   : {"message":str(e)},
                'status_http': 400
            }
            
        return response