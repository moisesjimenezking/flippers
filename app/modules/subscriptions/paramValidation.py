from .  import formValidation

class ParamValidation:

    # #* Reglas de parametros para el Get de token
    def subscriptionsGetRute(cls):
        param = {
            'required':set(),
            'optional':{
                'username',
                'code',
                'id'
            }
        }
        
        return param
    
    #* Reglas de parametros para el POST de token
    def subscriptionsPostRute(cls):
        param = {
            'required':{
                'username',
                'code'
            },
            'optional':{
                'operation_number'
            },
        }
        
        return param
    
    @classmethod
    def ValidationParam(cls, data, rute):
        try:
            #respuesta por defecto True
            response = {
                'response'   : {"message":True},
                'status_http': 200
            }
            
            listFuntion = {
                '/getSubscriptions'  : 'subscriptionsGetRute',
                '/postSubscriptions' : 'subscriptionsPostRute',
            }
            
            if(rute in listFuntion):
                method = getattr(ParamValidation, listFuntion[rute])
                params = method(cls)
                
                if(bool(params['required'])):
                    for key in params['required']:
                        if(key not in data):
                            raise Exception(key+" es un parametro requerido")

                setMerge = params["required"].union(params['optional']) 
                    
                if(bool(data)):
                    for key in data:
                        if(key not in setMerge):
                            raise Exception(key+" es un parametro no permitido")
                        
                if bool(data):
                    validationForm = formValidation.FormValidation(data, rute)
                    if(validationForm["status_http"] != 200):
                        raise Exception(validationForm["response"]["message"])

        except Exception as e:
            response = {
                'response'   : {"message":str(e)},
                'status_http': 406
            }
            
        return response