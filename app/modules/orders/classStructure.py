from create_app import db
from typing import Sequence
from datetime import datetime
from modules.subscriptions.classStructure import SubscriptionsClass
from modules.bots.classStructure import BootsClass
from modules.delivery.classStructure import DeliveryClass

class OrdersClass(db.Model):
    __tablename__ = 'orders'
    
    #? STRUCTURE DB TABLE USER
    id               = db.Column(db.Integer, primary_key=True)
    product_add_json = db.Column(db.JSON,    nullable=True)
    delivery_id      = db.Column(db.Integer, db.ForeignKey('delivery.id'), nullable=True)
    status_id        = db.Column(db.Integer, default=2)
    datetime         = db.Column(db.TIMESTAMP, default=datetime.utcnow)
    datetime_update  = db.Column(db.TIMESTAMP, nullable=True)
 
    # status = db.relationship(UserStatus, lazy='select')
    delivery = db.relationship(DeliveryClass, lazy='select', uselist=False)
    # bots = db.relationship(BootsClass, lazy='select', uselist=False)
#  primaryjoin='and_(BootsClass.status_id==2)'
    @property
    def serialize(self):
        return{
            'id'              : self.id,
            'product_add_json': self.product_add_json,
            'delivery_id'     : self.delivery_id,
            'status_id'       : self.status_id,
            'datetime'        : self.datetime,
            'datetime_update' : self.datetime_update,
            
            # # * Llaves foraneas
            'delivery': None if self.delivery is None else self.delivery.serialize,
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
        
        orderBy = getattr(OrdersClass, 'id')
        if 'order_by' in filters:
            orderBy = getattr(OrdersClass, filters['order_by'])
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
        users = OrdersClass.query.filter_by(id=param).first()
        return users
    
    #* Metodo de consulta GET en users permite filtros estandars y exactos
    #* En caso de que la coincidencia sea 1 se retorna un obj
    #* En caso de que la coincidencia sea mayor a 1 se retorna un array de obj
    @classmethod
    def getDataFirst(cls, param):
        users = OrdersClass.query.filter_by(id=param).first()
        return users
     
    #* Metodo de consulta GET en users permite filtros estandars y exactos
    #* En caso de que la coincidencia sea 1 se retorna un obj
    #* En caso de que la coincidencia sea mayor a 1 se retorna un array de obj
    @classmethod
    def getData(cls, **filters):
        users: Sequence[OrdersClass] = OrdersClass.query.filter_by(**filters).all()
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
        if 'username' in cols:
            username = OrdersClass.query.filter_by(username=cols["username"]).first()
            if username is not None:
                return{'message':'El nombre de usuario ya se encuentra registrado en la plataforma'}
            
        if 'email' in cols:
            email = OrdersClass.query.filter_by(email=cols["email"]).first()
            if email is not None:
                return{'message':'El Email ya se encuentra registrado en la plataforma'}

        users = cls.post(**cols)
        return users
#     # Crear una nueva venta
# new_sale = SalesClass(product_id=1, cantidad=10)

# # Agregar la venta a la sesión y confirmar los cambios
# db.session.add(new_sale)
# db.session.commit()

# # Obtener el ID de la venta recién agregada
# new_sale_id = new_sale.id
# # Verificar que la venta se haya guardado correctamente
# new_sale = SalesClass.query.filter_by(id=new_sale_id).first()
