from create_app import db
from typing import Sequence
from datetime import datetime


class ChatterInteractionClass(db.Model):
    __tablename__ = 'chatter_interaction'
    
    
    #? STRUCTURE DB TABLE USER
    id              = db.Column(db.Integer,     primary_key=True)
    bot_id          = db.Column(db.Integer,     nullable=False)
    chatter_phone   = db.Column(db.String(20),  nullable=True)
    question        = db.Column(db.Text,  nullable=True)
    response         = db.Column(db.Text,  nullable=True)
    datetime        = db.Column(db.TIMESTAMP, default=datetime.utcnow)
 
    # status = db.relationship(UserStatus, lazy='select')
    
    @property
    def serialize(self):
        return{
            'id'              : self.id,
            'bot_id'          : self.bot_id,
            'chatter_phone'   : self.chatter_phone,
            'question'        : self.question,
            'response'        : self.response,
            'datetime'        : self.datetime,
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
        
        orderBy = getattr(ChatterInteractionClass, 'id')
        if 'order_by' in filters:
            orderBy = getattr(ChatterInteractionClass, filters['order_by'])
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
        users = ChatterInteractionClass.query.filter_by(name=param).first()
        return users
     
    #* Metodo de consulta GET en users permite filtros estandars y exactos
    #* En caso de que la coincidencia sea 1 se retorna un obj
    #* En caso de que la coincidencia sea mayor a 1 se retorna un array de obj
    @classmethod
    def getData(cls, **filters):
        bots: Sequence[ChatterInteractionClass] = ChatterInteractionClass.query.filter_by(**filters).all()
        bots = [bot.serialize for bot in bots]
        return bots
    
    #* Metodo de actualizacion de usuarios
    #* Es requerido el ID del usuario
    def putData(data):
        db.session.commit()
        user = {"id":data.id}
        users = ChatterInteractionClass.getData(**user)
        return users
    
    #* Metodo Indterno para el registro de usuarios
    @classmethod
    def post(cls, **cols):
        bot = cls(**cols)
        db.session.add(bot)
        db.session.commit()
        bot = cls.getData(**cols)
        return bot

    #* Metodo Externo para el registro de usuarios 
    #* Este metodo comprueba la existencia de un usuario en la base de datos
    #* En caso de existir no se procede con el registro
    @classmethod
    def postData(cls, **cols):
        bot = cls.post(**cols)
        return bot