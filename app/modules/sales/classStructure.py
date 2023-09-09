from create_app import db
from typing import Sequence
from datetime import datetime, timedelta
from modules.orders.classStructure import OrdersClass
from modules.product.classStructure import ProductClass
from modules.chatters.classStructure import ChattersClass
from .statusCodes import CodeID, Code

class SalesClass(db.Model):
    __tablename__ = 'sales'
    
    #? STRUCTURE DB TABLE PLANS
    id              = db.Column(db.Integer,                         primary_key=True)
    user_id         = db.Column(db.Integer,                         nullable=False)
    bot_id          = db.Column(db.Integer,                         nullable=False)
    orders_id       = db.Column(db.Integer,                         db.ForeignKey('orders.id'), nullable=False)
    product_id      = db.Column(db.Integer,                         db.ForeignKey('products.id'), nullable=True)
    price           = db.Column(db.DECIMAL(precision=13, scale=2),  nullable=False, default=0)
    currency_code   = db.Column(db.Text(10),                        nullable=True)
    phone_chatters  = db.Column(db.Text(20),                        db.ForeignKey('chatters.phone'), nullable=False)
    status_id       = db.Column(db.Integer,                         default=3)
    datetime        = db.Column(db.TIMESTAMP,                       default=datetime.utcnow)
    datetime_update = db.Column(db.TIMESTAMP,                       nullable=True)
 
    order       = db.relationship(OrdersClass, lazy='select', uselist=False)
    product     = db.relationship(ProductClass, lazy='select', uselist=False)
    chatters    = db.relationship(ChattersClass, lazy='select', uselist=False)
    
    @property
    def serialize(self):
        return{
            'id'              : self.id,
            'user_id'         : self.user_id,
            'bot_id'          : self.bot_id,
            'orders_id'       : self.orders_id,
            'product_id'      : self.product_id,
            'price'           : self.price,
            'phone_chatters'  : self.phone_chatters,
            'currency_code'   : self.currency_code,
            'status_id'       : CodeID(self.status_id),
            'datetime'        : self.datetime,
            'datetime_update' : self.datetime_update,
            
            # * Llaves foraneas
            'order': None if self.order is None else self.order.serialize,
            'product': None if self.product is None else self.product.serialize,
            'chatters': None if self.chatters is None else self.chatters.serialize,
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
        
        orderBy = getattr(SalesClass, 'id')
        if 'order_by' in filters:
            orderBy = getattr(SalesClass, filters['order_by'])
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
        sale = SalesClass.query.filter_by(id=param).first()
        return sale
     
    @classmethod
    def getDataFirst(cls, param):
        sale = SalesClass.query.filter_by(id=param).first()
        return sale.serialize
        
    #* Metodo de consulta GET en users permite filtros estandars y exactos
    #* En caso de que la coincidencia sea 1 se retorna un obj
    #* En caso de que la coincidencia sea mayor a 1 se retorna un array de obj
    @classmethod
    def getData(cls, **filters):
        sales: Sequence[SalesClass] = SalesClass.query.filter_by(**filters).order_by(SalesClass.id.desc()).all()
        sales = [sale.serialize for sale in sales]
        return sales
    
    
    @classmethod
    def getDataTime(cls, user_id, datetimeEnd, datetimeStart):
        sales = SalesClass.query.filter_by(user_id=user_id, status_id=2).filter(SalesClass.datetime <= datetimeEnd, SalesClass.datetime >= datetimeStart).order_by(SalesClass.id.desc()).all()
        sales = [sale.serialize for sale in sales]
        return sales
    
    
    #* Metodo Indterno para el registro de usuarios
    @classmethod
    def post(cls, **cols):
        sales = cls(**cols)
        db.session.add(sales)
        db.session.commit()
        return sales.serialize


    #* Metodo Externo para el registro de usuarios 
    #* Este metodo comprueba la existencia de un usuario en la base de datos
    #* En caso de existir no se procede con el registro
    @classmethod
    def postData(cls, **cols):
        # if SubscriptionsClass.query.filter_by(**cols).first() is not None:
        #     return{'message':'El usuario existe en la plataforma'}

        sales = cls.post(**cols)
        return sales
    
    #* Metodo de actualizacion de usuarios
    #* Es requerido el ID del usuario
    def putData(data):
        db.session.commit()
        return data.serialize
    
    #* Client fidelity
    @classmethod
    def getDataFidelity(cls, phone):
        fecha_limite = datetime.now() - timedelta(days=30)
        sales = SalesClass.query.filter_by(phone_chatters=phone, status_id=Code("SOLD")).filter(SalesClass.datetime > fecha_limite).all()
        return [sale.serialize for sale in sales]