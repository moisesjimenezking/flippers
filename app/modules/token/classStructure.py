from create_app import db
from typing import Sequence
from datetime import datetime
from modules.user.classStructure import UserClass
from .statusCodes import CodeID
import logging

logging.basicConfig(level=logging.DEBUG)
class TokenClass(db.Model):
    __tablename__ = 'token'
    
    #? STRUCTURE DB TABLE USER
    id              = db.Column(db.Integer,     primary_key=True)
    user_id         = db.Column(db.Integer,     db.ForeignKey('user.id'), nullable=False)
    hash            = db.Column(db.Text,        nullable=False)
    refresh_hash    = db.Column(db.Text,        nullable=True)
    time_exp        = db.Column(db.TIMESTAMP,   nullable=False)
    status_id       = db.Column(db.Integer,     default=2)
    datetime        = db.Column(db.TIMESTAMP,   default=datetime.utcnow)
    datetime_update = db.Column(db.TIMESTAMP,   nullable=True)
 
    user = db.relationship(UserClass, lazy='select')
    
    @property
    def serialize(self):
        return{
            'id'              : self.id,
            'user_id'         : self.user_id,
            'token'           : self.hash,
            'refresh_token'   : self.refresh_hash,
            'time_exp'        : self.time_exp.strftime('%Y-%m-%d %H:%M:%S'),
            'status_id'       : CodeID(self.status_id),
            'datetime'        : self.datetime,
            'datetime_update' : self.datetime_update,
            
            # * Llaves foraneas
            'user': self.user.serialize
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
        
        orderBy = getattr(TokenClass, 'id')
        if 'order_by' in filters:
            orderBy = getattr(TokenClass, filters['order_by'])
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
        
    #* Metodo de consulta GET en token permite solo user_id
    @classmethod
    def getData(cls, **filters):
        tokens: Sequence[TokenClass] = TokenClass.query.filter_by(**filters).all()
        tokens = [token.serialize for token in tokens]
        return tokens
    
        
    #* Metodo para crear los tokens
    @classmethod
    def post(cls, **cols):
        tokens = cls(**cols)
        db.session.add(tokens)
        db.session.commit()
        return tokens.serialize
    
    #* Metodo para crear los tokens
    @classmethod
    def postRefresh(cls, **cols):
        tokens = cls(**cols)
        db.session.add(tokens)
        db.session.commit()
        tokens = tokens.serialize
        tokens.pop("user")
        tokens.pop("datetime")
        tokens.pop("datetime_update")
        return tokens