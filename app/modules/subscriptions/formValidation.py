from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, IntegerField, EmailField
from wtforms.validators import Length, Regexp, NumberRange, Optional

class FormValidation(FlaskForm):
    id               = IntegerField('id')
    user_id          = IntegerField('user_id')
    username         = StringField('username')
    code             = StringField('code')
    operation_number = StringField('operation_number')
    plans_id         = IntegerField('plans_id')
    transaction_id   = IntegerField('transaction_id')
    datetime_start   = StringField('datetime_start')
    datetime_end     = StringField('datetime_end')


class GetUserForm(FormValidation):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        #* username
        if self.username.data is not None:
            self.username.validators = [Length(min=3, max=60, message="La longitud mínima es 3 y máxima es 60")]

class PostSubscriptionsForm(FormValidation):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        #* username
        self.username.validators = [Length(min=3, max=60, message="La longitud mínima es 3 y máxima es 60")]
        
        #* code
        self.code.validators = [Length(min=2, max=20, message="La longitud mínima es 2 y máxima es 20")]
        
        if self.operation_number.data is not None:
            self.operation_number.validators = [
                Regexp(
                    r'^\d+$',
                    message = "solo debe contener numericos"
                ),
                Length(min=2, max=20, message="La longitud mínima es 2 y máxima es 20")
            ]
           
def FormValidation(data, route):
    try:
        listFunction = {
            '/getUser' : GetUserForm,
            '/postSubscriptions' : PostSubscriptionsForm,
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
