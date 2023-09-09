from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, IntegerField, EmailField
from wtforms.validators import Length, Regexp, NumberRange, Optional

class FormValidation(FlaskForm):
    username        = StringField('username')
    email           = StringField('email')
    passwd          = StringField('passwd')
    fullname        = StringField('fullname')
    phone           = StringField('phone')
    id              = IntegerField('id')
    verified_phone  = IntegerField('verified_phone')
    verified_email  = IntegerField('verified_email')


class GetTokenForm(FormValidation):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        #* username
        if self.username.data is not None:
            self.username.validators = [Length(min=3, max=60, message="La longitud mínima es 3 y máxima es 60")]

class PostTokenForm(FormValidation):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        #* username
        self.username.validators = [
            Regexp(
                r'^[a-z0-9_]{6,12}$',
                message="""
                    1) 6 a 12 caracteres
                    2) Al menos 3 letras minúsculas (SOLO MINÚSCULAS)
                    3) Al menos un número
                    """
            )
        ]
        
        #* passwd
        self.passwd.validators = [
            Regexp(
                r'^(?!.*\s)(?=.*?[A-Z]{1,})(?=.*?[a-z]{1,})(?=.*?[0-9]{1,}).{6,16}$',
                message= """
                    1) Al menos una letra mayúscula
                    2) Al menos una letra minúscula
                    3) Al menos un número
                    4) Caracteres especiales (OPCIONALES)
                    5) 6 A 16 CARACTERES
                    """
            )
        ]   
        
def FormValidation(data, route):
    try:
        listFunction = {
            '/getToken'  : GetTokenForm,
            '/postToken' : PostTokenForm,
        }

        if route in listFunction:
            form_class = listFunction[route]
            form = form_class(data=data)
            if not form.validate():
                for field_name, field_errors in form.errors.items():
                    if field_name != 'csrf_token':
                        raise Exception(f"Error en el campo '{field_name}': {', '.join(field_errors)}")
                    
        response = {
            'response': {"message": "OK"},
            'status_http': 200
        }

    except Exception as e:
        response = {
            'response': {"message": str(e)},
            'status_http': 406
        }

    return response
