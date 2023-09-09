from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, IntegerField, EmailField, DecimalField
from wtforms.validators import Length, Regexp, NumberRange, Optional

class FormValidationSales(FlaskForm):
    #* Se asigna los campos, a evaluar y el tipo de dato
    id              = IntegerField('id')
    user_id         = IntegerField('user_id')
    orders_id       = IntegerField('orders_id')
    bot_id          = IntegerField('bot_id')
    product_id      = IntegerField('product_id')
    price           = DecimalField('price')
    currency_code   = StringField('currency_code')    
    phone_chatters  = StringField('phone_chatters')
    status_id       = StringField('status_id')

#* Clase encargada de las validaciones de formulario del GET
class GetSalesForm(FormValidationSales):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

#* Clase encargada de las validaciones de formulario del POST
class PostSalesForm(FormValidationSales):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        #* phone_chatters
        if self.phone_chatters.data is not None:
            self.phone_chatters.validators = [Length(min=11, max=12, message="La longitud mínima es 11 y máxima es 12")]
            
#* Clase encargada de las validaciones de formulario del PUT
class PutSalesForm(FormValidationSales):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
     
#* Función encargada de llamar a las clases para validar el formulario según el método   
def FormValidation(data, route):
    try:
        #* Lista que almacena las clases que serán llamadas según el método
        listFunction = {
            '/getSales' : GetSalesForm,
            '/postSales': PostSalesForm,
            '/putSales':  PutSalesForm
        }

        #* De existir un error en el formulario se captura y se retorna
        if route in listFunction:
            form_class = listFunction[route]
            form = form_class(data=data)
            if not form.validate():
                for field_name, field_errors in form.errors.items():
                    if field_name != 'csrf_token':
                        raise Exception(f"Error en el campo '{field_name}': {', '.join(field_errors)}")
              
        #* Respuesta por defecto en caso de no ocurrir ningún error      
        response = {
            'response': {"message": "OK"},
            'status_http': 200
        }

    except Exception as e:
        response = {
            'response': {"message": str(e)},
            'status_http': 400
        }

    return response
