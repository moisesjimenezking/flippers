from create_app import db
from typing import Sequence
from datetime import datetime
from .statusCodes import CodeID
from .categoryCodes import CategoryID
from sqlalchemy import desc, func
import logging

logging.basicConfig(level=logging.DEBUG)
class ticketsClass(db.Model):
    __tablename__ = 'tickets'
    
    
    #? STRUCTURE DB TABLE USER
    id              = db.Column(db.Integer,     primary_key=True)
    category_id     = db.Column(db.Integer,     default=3)
    user_id         = db.Column(db.Integer,     nullable=False)
    chatter_id      = db.Column(db.Integer,     nullable=False)
    message         = db.Column(db.Text,        nullable=True)
    info            = db.Column(db.JSON,        nullable=True)
    status_id       = db.Column(db.Integer,     default=1)
    datetime        = db.Column(db.TIMESTAMP,   default=datetime.utcnow)
    datetime_update = db.Column(db.TIMESTAMP,   nullable=True)
 
    # company         = db.relationship(CompanyClass,       lazy='select', uselist=False)
    # subscriptions   = db.relationship(SubscriptionsClass, lazy='select', uselist=False)


    @property
    def serialize(self):
        return{
            'id'              : self.id,
            'category_id'     : CategoryID(self.category_id),
            'user_id'         : self.user_id,
            'chatter_id'      : self.chatter_id,
            'message'         : self.message,
            'info'            : self.info,
            'status_id'       : CodeID(self.status_id),
            'datetime'        : self.datetime,
            'datetime_update' : self.datetime_update,
            
            # * Llaves foraneas
            # 'bots'          : None   if self.bots          is None else self.bots.serialize,
            # 'notification'  : list() if self.notification  is None else [notifications.serialize for notifications in self.notification if notifications.status_id == 2],
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
        
        orderBy = getattr(UserClass, 'id')
        if 'order_by' in filters:
            orderBy = getattr(UserClass, filters['order_by'])
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
    def getDataFirstPut(cls, param):
        users = ticketsClass.query.filter_by(id=param).first()
        return users
     
    #* Metodo de consulta GET en users permite filtros estandars y exactos
    #* En caso de que la coincidencia sea 1 se retorna un obj
    #* En caso de que la coincidencia sea mayor a 1 se retorna un array de obj
    @classmethod
    def getData(cls, **filters):
        prepareFilter = cls.prepareFilters(**filters)
        filters     = prepareFilter["filters"]
        page        = prepareFilter["page"]
        limit       = prepareFilter["limit"]
        orderBy     = prepareFilter["orderBy"]
        typeOrderBy = prepareFilter["typeOrderBy"]
            
        users: Sequence[ticketsClass] = ticketsClass.query.filter_by(**filters).\
            order_by(desc(orderBy) if typeOrderBy else orderBy).\
            offset(page).limit(limit).all()
        
        users = [user.serialize for user in users]
        return users
    
    #* Metodo Indterno para el registro de usuarios
    @classmethod
    def post(cls, **cols):
        users = cls(**cols)
        db.session.add(users)
        db.session.commit()
        return users.serialize

    #* Metodo Externo para el registro de usuarios 
    #* Este metodo comprueba la existencia de un usuario en la base de datos
    #* En caso de existir no se procede con el registro
    @classmethod
    def postData(cls, **cols):
        # if 'username' in cols:
        #     username = ticketsClass.query.filter_by(username=cols["username"]).first()
        #     if username is not None:
        #         return{'message':'El nombre de usuario ya se encuentra registrado en la plataforma'}
            
        # if 'email' in cols:
        #     email = ticketsClass.query.filter_by(email=cols["email"]).first()
        #     if email is not None:
        #         return{'message':'El Email ya se encuentra registrado en la plataforma'}
            
        # if 'phone' in cols:
        #     phone = ticketsClass.query.filter_by(phone=cols["phone"]).first()
        #     if phone is not None:
        #         return{'message':'El telefono ya se encuentra registrado en la plataforma'}

        users = cls.post(**cols)
        return users