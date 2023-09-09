from create_app import db
from typing import Sequence
from datetime import datetime
from . statusCodes import CodeID

class CommandsClass(db.Model):
    __tablename__ = 'commands'
    
    #? STRUCTURE DB TABLE PLANS
    id              = db.Column(db.Integer,     primary_key=True)
    code            = db.Column(db.Text(60),   nullable=False)
    bot_id          = db.Column(db.Integer, nullable=True)
    message         = db.Column(db.JSON, nullable=False)
    file            = db.Column(db.String(4294967295), nullable=True)
    status_id       = db.Column(db.Integer, default=1)
    datetime        = db.Column(db.TIMESTAMP, default=datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
    datetime_update = db.Column(db.TIMESTAMP, nullable=True)

    # status = db.relationship(UserStatus, lazy='select')
    
    @property
    def serialize(self):
        return{
            'id'              : self.id,
            'code'            : self.code,
            'bot_id'          : self.bot_id,
            'message'         : self.message,
            'file'            : self.file,
            'status_id'       : CodeID(self.status_id),
            'datetime'        : self.datetime,
            'datetime_update' : self.datetime_update
        }
        
    @classmethod
    def prepareFilters(cls, **filters):
        limit = 10
        if 'limit' in filters:
            limit = filters['limit']
            filters.pop('limit')
        
        page = 0
        if 'page' in filters:
            page = (int(filters['page']) - 1) * int(limit)
            filters.pop('page')
        
        orderBy = getattr(CommandsClass, 'id')
        if 'order_by' in filters:
            orderBy = getattr(CommandsClass, filters['order_by'])
            filters.pop('order_by')
              
        typeOrderBy = True
        if 'type_order_by' in filters:
            typeOrderBy = True if filters['type_order_by'].lower() == 'desc' else False
            filters.pop('type_order_by')
            
        return{
            'filters'       : filters,
            'page'          : page,
            'orderBy'       : orderBy,
            'typeOrderBy'   : typeOrderBy,
            'limit'         : limit
        }
        
    #* Metodo de consulta GET en users permite filtros estandars y exactos
    #* En caso de que la coincidencia sea 1 se retorna un obj
    #* En caso de que la coincidencia sea mayor a 1 se retorna un array de obj
    @classmethod
    def getData(cls, **filters):
        sales: Sequence[CommandsClass] = CommandsClass.query.filter_by(**filters).all()
        sales = [sale.serialize for sale in sales]
        return sales
    
     #* Metodo Indterno para el registro de usuarios
    @classmethod
    def post(cls, **cols):
        sales = cls(**cols)
        db.session.add(sales)
        db.session.commit()
        cols.pop("message")
        sales = cls.getData(**cols)
        return sales

    #* Metodo Externo para el registro de usuarios 
    #* Este metodo comprueba la existencia de un usuario en la base de datos
    #* En caso de existir no se procede con el registro
    @classmethod
    def postData(cls, **cols):
        # if SubscriptionsClass.query.filter_by(**cols).first() is not None:
        #     return{'message':'El usuario existe en la plataforma'}

        sales = cls.post(**cols)
        return sales
    
    #* Metodo de consulta GET en users permite filtros estandars y exactos
    #* En caso de que la coincidencia sea 1 se retorna un obj
    #* En caso de que la coincidencia sea mayor a 1 se retorna un array de obj
    @classmethod
    def getDataFirst(cls, param):
        users = CommandsClass.query.filter_by(id=param).first()
        return users
    
    @classmethod
    def deletData(cls, data):
        db.session.delete(data)
        db.session.commit()
        user = CommandsClass.query.filter_by(id=data.id).first()
        if user is None:
            return{'message':'El comando ha sido eliminado.'}
        else:
            return user.serialize
        
    #* Metodo de actualizacion de usuarios
    #* Es requerido el ID del usuario
    def putData(data):
        db.session.commit()
        data = CommandsClass.query.filter_by(id=data.id).first()

        return data.serialize
    
    @classmethod
    def botCommands(cls, bot_id):
        sales: Sequence[CommandsClass] = CommandsClass.query.filter_by(bot_id=bot_id).all()
        response = dict()
        for sale in sales:
            response.update({sale.code:sale.message[0] if isinstance(sale.message, list) else sale.message})

        return response