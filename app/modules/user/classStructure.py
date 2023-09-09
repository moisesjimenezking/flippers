from create_app import db
from typing import Sequence
from datetime import datetime
from modules.subscriptions.classStructure import SubscriptionsClass
from modules.bots.classStructure import BootsClass
from modules.company.classStructure import CompanyClass
from modules.notification.classStructure import NotificationClass
from .statusCodes import CodeID
from sqlalchemy import desc, func
import logging

logging.basicConfig(level=logging.DEBUG)
class UserClass(db.Model):
    __tablename__ = 'user'
    
    
    #? STRUCTURE DB TABLE USER
    id              = db.Column(db.Integer,     primary_key=True)
    account_type    = db.Column(db.Text,        default="business")
    username        = db.Column(db.String(64),  nullable=False)
    fullname        = db.Column(db.String(150), nullable=False)
    passwd          = db.Column(db.String(64),  nullable=False)
    email           = db.Column(db.String(64),  nullable=True)
    verified_email  = db.Column(db.Integer,     default=0)
    phone           = db.Column(db.String(64),  nullable=True)
    verified_phone  = db.Column(db.Integer,     default=0)
    company_id      = db.Column(db.Integer,     db.ForeignKey('company.id'), nullable=True)
    status_id       = db.Column(db.Integer,     default=1)
    datetime        = db.Column(db.TIMESTAMP,   default=datetime.utcnow)
    datetime_update = db.Column(db.TIMESTAMP,   nullable=True)
 
    company         = db.relationship(CompanyClass,       lazy='select', uselist=False)
    subscriptions   = db.relationship(SubscriptionsClass, lazy='select', uselist=False)
    bots            = db.relationship(BootsClass,         lazy='select', uselist=False)
    notification    = db.relationship(NotificationClass,  lazy='select', uselist=True)


    @property
    def serialize(self):
        return{
            'id'              : self.id,
            'account_type'    : self.account_type,
            'username'        : self.username,
            'fullname'        : self.fullname,
            'passwd'          : self.passwd,
            'email'           : self.email,
            'verified_email'  : self.verified_email,
            'phone'           : self.phone,
            'company_id'      : self.company_id,
            'verified_phone'  : self.verified_phone,
            'status_id'       : CodeID(self.status_id),
            'datetime'        : self.datetime,
            'datetime_update' : self.datetime_update,
            
            # * Llaves foraneas
            'company'       : None   if self.company       is None else self.company.serialize,
            'subscriptions' : None   if self.subscriptions is None else self.subscriptions.serialize,
            'bots'          : None   if self.bots          is None else self.bots.serialize,
            'notification'  : list() if self.notification  is None else [notifications.serialize for notifications in self.notification if notifications.status_id == 2],
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
            'filters'       : dict() if len(filters) == 0 else filters,
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
        users = UserClass.query.filter_by(id=param).first()
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
            
        users: Sequence[UserClass] = UserClass.query.filter_by(**filters).\
            order_by(desc(orderBy) if typeOrderBy else orderBy).\
            offset(page).limit(limit).all()
        
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
        return users.serialize

    #* Metodo Externo para el registro de usuarios 
    #* Este metodo comprueba la existencia de un usuario en la base de datos
    #* En caso de existir no se procede con el registro
    @classmethod
    def postData(cls, **cols):
        if 'username' in cols:
            username = UserClass.query.filter_by(username=cols["username"]).first()
            if username is not None:
                return{'message':'El nombre de usuario ya se encuentra registrado en la plataforma'}
            
        if 'email' in cols:
            email = UserClass.query.filter_by(email=cols["email"]).first()
            if email is not None:
                return{'message':'El Email ya se encuentra registrado en la plataforma'}
            
        if 'phone' in cols:
            phone = UserClass.query.filter_by(phone=cols["phone"]).first()
            if phone is not None:
                return{'message':'El telefono ya se encuentra registrado en la plataforma'}

        users = cls.post(**cols)
        return users

    @classmethod
    def getUserAllData(cls):
        users: Sequence[UserClass] = UserClass.query.filter(UserClass.company_id.isnot(None)).all()
        response = list()
        for user in users:
            companyAux = None if user.company is None else user.company.serialize
            botAux = None if user.bots is None else user.bots.serialize
            if companyAux is not None and botAux is not None:
                aux = {
                    "image_url"     : None if companyAux is None else companyAux["image_url"],
                    "name"          : None if companyAux is None else companyAux["company_name"],
                    "description"   : None if botAux     is None else botAux["objetive"],
                    "link"          : None if botAux     is None else botAux["social_links"],
                    "phone_number"  : None if botAux     is None else botAux["phone"],
                    "satisfaction"  : None if companyAux is None else companyAux["satisfaction"]
                }
                
                response.append(aux)
        
        return response
    
    @classmethod
    def getDataFirst(cls, param):
        users = UserClass.query.filter_by(id=param).first()
        return users.serialize
    
    @classmethod
    def deletData(cls, data):
        db.session.delete(data)
        db.session.commit()
        user = UserClass.query.filter_by(id=data.id).first()
        if user is None:
            return{'message':'La cuenta ha sido eliminada.'}
        else:
            return user.serialize
        
# class UserLogClass(db.Model):
#     __tablename__ = 'user_log'
    
    
#     #? STRUCTURE DB TABLE USER
#     id              = db.Column(db.Integer, primary_key=True)
#     user_id         = db.Column(db.Integer, nullable=False)
#     username        = db.Column(db.String(64), nullable=False)
#     fullname        = db.Column(db.String(150), nullable=False)
#     passwd          = db.Column(db.String(64), nullable=False)
#     email           = db.Column(db.String(64), nullable=False)
#     direction       = db.Column(db.Text, nullable=True)
#     verified_email  = db.Column(db.Integer, default=0)
#     phone           = db.Column(db.String(64), nullable=False)
#     verified_phone  = db.Column(db.Integer, default=0)
#     status_id       = db.Column(db.Integer, default=1)
#     datetime        = db.Column(db.TIMESTAMP, default=datetime.utcnow)
#     datetime_update = db.Column(db.TIMESTAMP, nullable=True)
 
#     @property
#     def serialize(self):
#         return{
#             'id'              : self.id,
#             'user_id'         : self.user_id,
#             'username'        : self.username,
#             'fullname'        : self.fullname,
#             'passwd'          : self.passwd,
#             'email'           : self.email,
#             'direction'       : self.direction,
#             'verified_email'  : self.verified_email,
#             'phone'           : self.phone,
#             'verified_phone'  : self.verified_phone,
#             'status_id'       : self.status_id,
#             'datetime'        : self.datetime,
#             'datetime_update' : self.datetime_update
#         }
    
    
#     @classmethod
#     def getDataFirst(cls, user_id, username):
#         users = UserLogClass.query.filter_by(user_id=user_id).filter(UserLogClass.username != username).order_by(UserLogClass.id.desc()).first()
#         return users.serialize