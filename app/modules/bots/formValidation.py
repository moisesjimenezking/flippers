from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, IntegerField, EmailField
from wtforms.validators import Length, Regexp, NumberRange, Optional

class FormValidationUser(FlaskForm):
    #* Se asigna los campos, a evaluar y el tipo de dato
    username        = StringField('username')
    email           = StringField('email')
    passwd          = StringField('passwd')
    fullname        = StringField('fullname')
    phone           = StringField('phone')
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
        self.username.validators = [Length(min=3, max=60, message="La longitud mínima es 3 y máxima es 60")]
        
        #* email
        self.email.validators = [
            Regexp(r'^[\w\.-]+@[\w\.-]+\.\w+$',message='Correo electrónico inválido'),
            Length(min=3, max=80, message="La longitud mínima es 3 y máxima es 80")
        ]
        
        #* passwd
        self.passwd.validators = [
            Regexp(
                r'^(?=.*\d{2,})(?=.*[a-zA-Z]{2,})(?=.*[A-Z])(?=.*[-_?!.*])[a-zA-Z\d_?!.*-]+$',
                message= "debe contener minimo 2 letras, 2 números, 1 letra mayúscula y un carácter especial '-_?!.*'"),
            
            Length(min=2, max=40, message="La longitud mínima es 2 y máxima es 40")
        ]
        
        #* fullname
        if self.fullname.data is not None:
            self.fullname.validators = [Length(min=3, max=60, message="La longitud mínima es 3 y máxima es 60")]
        
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
                    r'^(?=.*\d{2,})(?=.*[a-zA-Z]{2,})(?=.*[A-Z])(?=.*[-_?!.*])[a-zA-Z\d_?!.*-]+$',
                    message= "debe contener minimo 2 letras, 2 números, 1 letra mayúscula y un carácter especial '-_?!.*'"),
                Length(min=2, max=40, message="La longitud mínima es 2 y máxima es 40")
            ]
        
        #* fullname
        if self.fullname.data is not None:
            self.fullname.validators = [Length(min=3, max=60, message="La longitud mínima es 3 y máxima es 60")]
        
        #* phone
        if self.phone.data is not None:
            self.phone.validators = [Length(min=3, max=20, message="La longitud mínima es 3 y máxima es 20")]
        
        #* email
        if self.email.data is not None:
            self.email.validators = [
                Regexp(r'^[\w\.-]+@[\w\.-]+\.\w+$',message='Correo electrónico inválido'),
                Length(min=3, max=80, message="La longitud mínima es 3 y máxima es 80")
            ]
        
        #* verified_phone
        if self.verified_phone.data is not None:
            self.verified_phone.validators = [NumberRange(min=0, max=1, message="debe ser un booleano numérico 0 o 1")]
        
        #* verified_email
        if self.verified_email.data is not None:  
            self.verified_email.validators = [NumberRange(min=0, max=1, message="debe ser un booleano numérico 0 o 1")]
        
     
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
