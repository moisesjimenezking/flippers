from create_app import db
from typing import Sequence
from datetime import datetime
from .statusCodes import CodeID
# from modules.subscriptions.classStructure import SubscriptionsClass
# from modules.boots.classStructure import BootsClass

class DeliveryClass(db.Model):
    __tablename__ = 'delivery'
    
    
    #? STRUCTURE DB TABLE USER
    id              = db.Column(db.Integer, primary_key=True)
    direction       = db.Column(db.Text,    nullable=False)
    status_id       = db.Column(db.Integer, default=1)
    datetime        = db.Column(db.TIMESTAMP, default=datetime.utcnow)
    datetime_update = db.Column(db.TIMESTAMP, nullable=True)
 
    # status = db.relationship(UserStatus, lazy='select')
#     subscriptions = db.relationship(SubscriptionsClass, lazy='select', uselist=False)
#     bots = db.relationship(BootsClass, lazy='select', uselist=False)
# #  primaryjoin='and_(BootsClass.status_id==2)'
   
    @property
    def serialize(self):
        return{
            'id'              : self.id,
            'direction'       : self.direction,
            'status_id'       : CodeID(self.status_id),
            'datetime'        : self.datetime,
            'datetime_update' : self.datetime_update,
            
            # * Llaves foraneas
            # 'subscriptions': None if self.subscriptions is None else self.subscriptions.serialize,
            # 'bots': None if self.bots is None else self.bots.serialize,
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
        
        orderBy = getattr(DeliveryClass, 'id')
        if 'order_by' in filters:
            orderBy = getattr(DeliveryClass, filters['order_by'])
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
        users = DeliveryClass.query.filter_by(id=param).first()
        return users
     
    #* Metodo de consulta GET en users permite filtros estandars y exactos
    #* En caso de que la coincidencia sea 1 se retorna un obj
    #* En caso de que la coincidencia sea mayor a 1 se retorna un array de obj
    @classmethod
    def getData(cls, **filters):
        users: Sequence[DeliveryClass] = DeliveryClass.query.filter_by(**filters).all()
        users = [user.serialize for user in users]
        return users
    
    #* Metodo de actualizacion de usuarios
    #* Es requerido el ID del usuario
    def putData(data):
        db.session.commit()
        return data.serialize
    
    #* Metodo Indterno para el registro de usuarios
    @classmethod
    def post(cls, **cols):
        users = cls(**cols)
        db.session.add(users)
        db.session.commit()
        users = cls.getData(**{"id":users.id})
        return users

    #* Metodo Externo para el registro de usuarios 
    #* Este metodo comprueba la existencia de un usuario en la base de datos
    #* En caso de existir no se procede con el registro
    @classmethod
    def postData(cls, **cols):
        users = cls.post(**cols)
        return users