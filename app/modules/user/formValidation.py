from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, IntegerField, EmailField
from wtforms.validators import Length, Regexp, NumberRange, Optional

class FormValidationUser(FlaskForm):
    #* Se asigna los campos, a evaluar y el tipo de dato
    username        = StringField('username')
    email           = StringField('email')
    passwd          = StringField('passwd')
    fullname        = StringField('fullname')
    company_name    = StringField('company_name')
    phone           = StringField('phone')
    direction       = StringField('direction')
    id              = IntegerField('id')
    verified_phone  = IntegerField('verified_phone')
    verified_email  = IntegerField('verified_email')


#* Clase encargada de las validaciones de formulario del GET
class GetUserForm(FormValidationUser):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        #* username
        if self.username.data is not None:
            self.username.validators = [Length(min=3, max=60, message="La longitud mínima es 3 y máxima es 60")]


#* Clase encargada de las validaciones de formulario del POST
class PostUserForm(FormValidationUser):
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
        
        #* email
        self.email.validators = [
            Regexp(r'^[a-zA-Z0-9._-]+@[a-zA-Z0-9.-]+\.([a-zA-Z]{2,4})+$',message='Correo electrónico inválido'),
            Length(min=3, max=80, message="La longitud mínima es 3 y máxima es 80")
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
        
        #* fullname 
        if self.fullname.data is not None:
            self.fullname.validators = [
                Regexp(
                    r'^([A-Z]?)([a-z]){3,12}\s(([A-Z]{0,1})(([a-z]){3,12}\s?)){1,3}$',
                    message= """
                        \n1) Letra inicial en mayúscula o minúscula
                        \n2) Al menos un nombre con 3 caracteres mínimos y 12 caracteres máximos
                        \n3) Al menos un nombre con dos palabras, o sea, Nombre y Apellido
                        \n4) Hasta 4 palabras, o sea, los 2 Nombres y 2 Apellidos
                        """
                ),
            ]
        
        #* phone
        self.phone.validators = [Length(min=3, max=20, message="La longitud mínima es 3 y máxima es 20")]


#* Clase encargada de las validaciones de formulario del PUT
class PutUserForm(FormValidationUser):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        #* passwd
        if self.passwd.data is not None:
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
        
        #* fullname
        if self.fullname.data is not None:
            self.fullname.validators = [
                Regexp(
                    r'^([A-Z]?)([a-z]){3,12}\s(([A-Z]{0,1})(([a-z]){3,12}\s?)){1,3}$',
                    message= """
                        \n1) Letra inicial en mayúscula o minúscula
                        \n2) Al menos un nombre con 3 caracteres mínimos y 12 caracteres máximos
                        \n3) Al menos un nombre con dos palabras, o sea, Nombre y Apellido
                        \n4) Hasta 4 palabras, o sea, los 2 Nombres y 2 Apellidos
                        """
                ),
            ]
        
        #* phone
        if self.company_name.data is not None:
            self.company_name.validators = [Length(min=3, max=80, message="La longitud mínima es 3 y máxima es 20")]
            
        #* phone
        if self.phone.data is not None:
            self.phone.validators = [Length(min=3, max=20, message="La longitud mínima es 3 y máxima es 20")]
        
        #* email
        if self.email.data is not None:
            self.email.validators = [
                Regexp(r'^[a-zA-Z0-9._-]+@[a-zA-Z0-9.-]+\.([a-zA-Z]{2,4})+$',message='Correo electrónico inválido'),
                Length(min=3, max=80, message="La longitud mínima es 3 y máxima es 80")
            ]
        
        #* verified_phone
        if self.verified_phone.data is not None:
            self.verified_phone.validators = [NumberRange(min=0, max=1, message="debe ser un booleano numérico 0 o 1")]
        
        #* verified_email
        if self.verified_email.data is not None:  
            self.verified_email.validators = [NumberRange(min=0, max=1, message="debe ser un booleano numérico 0 o 1")]
            
        #* direction
        if self.direction.data is not None:
            self.direction.validator = Length(min=10, max=50, message="La longitud mínima es 10 y máxima es 50")
        
     
#* Función encargada de llamar a las clases para validar el formulario según el método   
def FormValidation(data, route):
    try:
        #* Lista que almacena las clases que serán llamadas según el método
        listFunction = {
            '/getUser' : GetUserForm,
            '/postUser': PostUserForm,
            '/putUser':  PutUserForm
        }

        #* De existir un error en el formulario se captura y se retorna
        if route in listFunction:
            form_class = listFunction[route]
            form = form_class(data=data)
            if not form.validate():
                for field_name, field_errors in form.errors.items():
                    if field_name != 'csrf_token':
                        field_name = "password" if field_name == "passwd" else field_name
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
