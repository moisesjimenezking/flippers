from create_app import db
from typing import Sequence
from datetime import datetime


class ClaimsClass(db.Model):
    __tablename__ = 'claims'
    
    #? STRUCTURE DB TABLE PLANS
    id              = db.Column(db.Integer,     primary_key=True)
    bot_id         = db.Column(db.Integer,     nullable=False)
    chatter_phone   = db.Column(db.Text(20),    nullable=False)
    message         = db.Column(db.Text,        nullable=True)
    response        = db.Column(db.Text,        nullable=True)
    status_id       = db.Column(db.Integer,     default=1)
    datetime        = db.Column(db.TIMESTAMP,   default=datetime.utcnow)
    datetime_update = db.Column(db.TIMESTAMP,   nullable=True)

    # status = db.relationship(UserStatus, lazy='select')
    @property
    def serialize(self):
        return{
            'id'              : self.id,
            'bot_id'          : self.bot_id,
            'chatter_phone'   : self.chatter_phone,
            'message'         : self.message,
            'response'        : self.response,
            'status_id'       : self.status_id,
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
        
        orderBy = getattr(ClaimsClass, 'id')
        if 'order_by' in filters:
            orderBy = getattr(ClaimsClass, filters['order_by'])
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
        sales: Sequence[ClaimsClass] = ClaimsClass.query.filter_by(**filters).all()
        sales = [sale.serialize for sale in sales]
        return sales
    
     #* Metodo Indterno para el registro de usuarios
    @classmethod
    def post(cls, **cols):
        sales = cls(**cols)
        db.session.add(sales)
        db.session.commit()
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
    
    @classmethod
    def getDataTime(cls, bot_id, datetimeStart, datetimeEnd):
        sales = ClaimsClass.query.filter_by(bot_id=bot_id).filter(ClaimsClass.datetime >= datetimeStart, ClaimsClass.datetime <= datetimeEnd).order_by(ClaimsClass.id.desc()).all()
        sales = [sale.serialize for sale in sales]
        return sales