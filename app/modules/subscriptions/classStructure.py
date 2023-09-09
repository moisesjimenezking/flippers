from create_app import db
from typing import Sequence
from datetime import datetime
# from modules.user.classStructure import UserClass
from modules.plans.classStructure import PlansClass


class SubscriptionsClass(db.Model):
    __tablename__ = 'subscriptions'
    
    #? STRUCTURE DB TABLE USER
    id              = db.Column(db.Integer,   primary_key=True)
    user_id         = db.Column(db.Integer,   db.ForeignKey('user.id'), nullable=False)
    plans_id        = db.Column(db.Integer,   db.ForeignKey('plans.id'), nullable=False)
    transaction_id  = db.Column(db.Integer,   nullable=True) #db.ForeignKey('transaction.id'),
    datetime_start  = db.Column(db.TIMESTAMP, nullable=True, default=datetime.utcnow)
    datetime_end    = db.Column(db.TIMESTAMP, nullable=True)#default=datetime.utcnow)
    status_id       = db.Column(db.Integer,   default=2)
    datetime        = db.Column(db.TIMESTAMP, default=datetime.utcnow)
    datetime_update = db.Column(db.TIMESTAMP, nullable=True)
 
    # user  = db.relationship(UserClass, lazy='select')
    plans = db.relationship(PlansClass, lazy='select')
    
    @property
    def serialize(self):
        return{
            'id'              : self.id,
            'user_id'         : self.user_id,
            'plans_id'        : self.plans_id,
            'transaction_id'  : self.transaction_id,
            'datetime_start'  : self.datetime_start,
            'datetime_end'    : self.datetime_end,
            'status_id'       : self.status_id,
            'datetime'        : self.datetime,
            'datetime_update' : self.datetime_update,
            # 'time_exp'        : self.time_exp.strftime('%Y-%m-%d %H:%M:%S'),

            # * Llaves foraneas
            # 'user': self.user.serialize,
            'plans': self.plans.serialize
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
        
        orderBy = getattr(SubscriptionsClass, 'id')
        if 'order_by' in filters:
            orderBy = getattr(SubscriptionsClass, filters['order_by'])
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
    def getDataFirst(cls, param):
        users = SubscriptionsClass.query.filter_by(user_id=param).first()
        return users
        
    #* Metodo de consulta GET en users permite filtros estandars y exactos
    #* En caso de que la coincidencia sea 1 se retorna un obj
    #* En caso de que la coincidencia sea mayor a 1 se retorna un array de obj
    @classmethod
    def getData(cls, **filters):
        subscriptions: Sequence[SubscriptionsClass] = SubscriptionsClass.query.filter_by(**filters).all()
        subscriptions = [subscription.serialize for subscription in subscriptions]
        return subscriptions
    
    #* Metodo de actualizacion de usuarios
    #* Es requerido el ID del usuario
    def putData(data):
        db.session.commit()
        return data.serialize
        
    #* Metodo Indterno para el registro de usuarios
    @classmethod
    def post(cls, **cols):
        subscriptions = cls(**cols)
        db.session.add(subscriptions)
        db.session.commit()
        subscriptions = cls.getData(**cols)
        return subscriptions

    #* Metodo Externo para el registro de usuarios 
    #* Este metodo comprueba la existencia de un usuario en la base de datos
    #* En caso de existir no se procede con el registro
    @classmethod
    def postData(cls, **cols):
        # if SubscriptionsClass.query.filter_by(**cols).first() is not None:
        #     return{'message':'El usuario existe en la plataforma'}

        subscriptions = cls.post(**cols)
        return subscriptions