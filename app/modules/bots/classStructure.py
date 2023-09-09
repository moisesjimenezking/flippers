from create_app import db
from typing import Sequence
from datetime import datetime
from .statusCodes import CodeID


class BootsClass(db.Model):
    __tablename__ = 'bots'
    
    
    #? STRUCTURE DB TABLE USER
    id              = db.Column(db.Integer,     primary_key=True)
    user_id         = db.Column(db.Integer,     db.ForeignKey('user.id'), nullable=True)
    ip              = db.Column(db.String(30),  nullable=True)
    name            = db.Column(db.String(150), nullable=False)
    phone           = db.Column(db.String(64),  nullable=False)
    qr              = db.Column(db.Text,        nullable=True)
    objetive        = db.Column(db.Text,        nullable=True)
    summary         = db.Column(db.Text,        nullable=True)
    threshold_sales = db.Column(db.Integer,     nullable=False, default=20)
    social_links    = db.Column(db.JSON,        nullable=True)
    chatters_active = db.Column(db.Integer,     nullable=True)
    web_page        = db.Column(db.Text,        nullable=True)
    bussiness_hours = db.Column(db.Text,        nullable=True)
    has_delivery    = db.Column(db.Integer,     nullable=False, default=1)
    has_descounts   = db.Column(db.Integer,     nullable=False, default=1)
    has_promotions  = db.Column(db.Integer,     nullable=False, default=1)
    status_id       = db.Column(db.Integer,     default=1)
    datetime        = db.Column(db.TIMESTAMP,   default=datetime.utcnow)
    datetime_update = db.Column(db.TIMESTAMP,   nullable=True)
 
    # status = db.relationship(UserStatus, lazy='select')
    
    @property
    def serialize(self):
        return{
            'id'              : self.id,
            'user_id'         : self.user_id,
            'ip'              : self.ip,
            'name'            : self.name,
            'phone'           : self.phone,
            'qr'              : self.qr,
            'objetive'        : self.objetive,
            'summary'         : self.summary,
            'threshold_sales' : self.threshold_sales,
            'social_links'    : self.social_links,
            'chatters_active' : self.chatters_active,
            'web_page'        : self.web_page,
            'bussiness_hours' : self.bussiness_hours,
            'has_delivery'    : bool(self.has_delivery),
            'has_descounts'   : bool(self.has_descounts),
            'has_promotions'  : bool(self.has_promotions),
            'status'          : CodeID(self.status_id),
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
        
        orderBy = getattr(BootsClass, 'id')
        if 'order_by' in filters:
            orderBy = getattr(BootsClass, filters['order_by'])
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
        users = BootsClass.query.filter_by(name=param).first()
        return users
    
    @classmethod
    def getDataFirstUser(cls, param):
        users = BootsClass.query.filter_by(user_id=param).first()
        return users.serialize
    
    @classmethod
    def getDataSearchBot(cls, **params):
        users = BootsClass.query.filter_by(**params).first()
        return users.serialize
     
    #* Metodo de consulta GET en users permite filtros estandars y exactos
    #* En caso de que la coincidencia sea 1 se retorna un obj
    #* En caso de que la coincidencia sea mayor a 1 se retorna un array de obj
    @classmethod
    def getData(cls, **filters):
        bots: Sequence[BootsClass] = BootsClass.query.filter_by(**filters).all()
        bots = [bot.serialize for bot in bots]
        return bots
    
    #* Metodo de actualizacion de usuarios
    #* Es requerido el ID del usuario
    def putData(data):
        db.session.commit()
        user = {"id":data.id}
        users = BootsClass.getData(**user)
        return users
    
    #* Metodo Indterno para el registro de usuarios
    @classmethod
    def post(cls, **cols):
        bot = cls(**cols)
        db.session.add(bot)
        db.session.commit()
        return bot.serialize

    #* Metodo Externo para el registro de usuarios 
    #* Este metodo comprueba la existencia de un usuario en la base de datos
    #* En caso de existir no se procede con el registro
    @classmethod
    def postData(cls, **cols):
        if BootsClass.query.filter_by(**cols).first() is not None:
            return{'message':'El boot existe en la plataforma'}
        bot = cls.post(**cols)
        return bot
    
    
    @classmethod
    def deletData(cls, data):
        db.session.delete(data)
        db.session.commit()
        company = BootsClass.query.filter_by(id=data.id).first()
        if company is None:
            return{'message':'La compañia ha sido eliminada.'}
        else:
            return company.serialize