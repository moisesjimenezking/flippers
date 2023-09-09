from create_app import db
from typing import Sequence
from datetime import datetime
from .statusCodes import CodeID, Code
from datetime import datetime, timedelta

import logging

logging.basicConfig(level=logging.DEBUG)

class TempCodeClass(db.Model):
    __tablename__ = 'temp_codes'
    
    
    #? STRUCTURE DB TABLE USER
    id              = db.Column(db.Integer,     primary_key=True)
    user_id         = db.Column(db.Integer,     nullable=False)
    type            = db.Column(db.String(30),  nullable=False)
    code            = db.Column(db.String(6),   nullable=False)
    status_id       = db.Column(db.Integer,     default=2)
    datetime        = db.Column(db.TIMESTAMP,   default=datetime.utcnow)
    datetime_update = db.Column(db.TIMESTAMP,   nullable=True)
 
    # status = db.relationship(UserStatus, lazy='select')
    
    @property
    def serialize(self):
        return{
            'id'              : self.id,
            'user_id'         : self.user_id,
            'type'            : self.type,
            'code'            : self.code,
            'status_id'       : CodeID(self.status_id),
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
        
        orderBy = getattr(TempCodeClass, 'id')
        if 'order_by' in filters:
            orderBy = getattr(TempCodeClass, filters['order_by'])
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
        tempCode = TempCodeClass.query.filter_by(name=param).first()
        return tempCode
     
    #* Metodo de consulta GET en users permite filtros estandars y exactos
    #* En caso de que la coincidencia sea 1 se retorna un obj
    #* En caso de que la coincidencia sea mayor a 1 se retorna un array de obj
    @classmethod
    def getData(cls, **filters):
        tempCodes: Sequence[TempCodeClass] = TempCodeClass.query.filter_by(**filters).all()
        tempCodes = [tempCode.serialize for tempCode in tempCodes]
        return tempCodes
    
    #* Metodo de actualizacion de usuarios
    #* Es requerido el ID del usuario
    def putData(data):
        db.session.commit()
        tempCodes = TempCodeClass.getData(**{"id":data.id})
        return tempCodes
    
    #* Metodo Indterno para el registro de usuarios
    @classmethod
    def post(cls, **cols):
        tempCodes = cls(**cols)
        db.session.add(tempCodes)
        db.session.commit()
        return tempCodes.serialize

    #* Metodo Externo para el registro de usuarios 
    #* Este metodo comprueba la existencia de un usuario en la base de datos
    #* En caso de existir no se procede con el registro
    @classmethod
    def postData(cls, **cols):
        if TempCodeClass.query.filter_by(**cols).first() is not None:
            return{'message':'El boot existe en la plataforma'}
        
        tempCodes = cls.post(**cols)
        return tempCodes
    
    @classmethod
    def getDataCode(cls, **filters):
        tempCode = TempCodeClass.query.filter_by(**filters).first()
        if tempCode is not None:
            if tempCode.status_id == 2:
                timeCurrent = datetime.now() 
                timeExpired = tempCode.datetime + timedelta(minutes=30)

                if timeCurrent > timeExpired:
                    setattr(tempCode, "status_id", 1)
                    db.session.commit()
                    return {"message":"El codigo ha expirado."}
            else:
                return {"message":"El codigo no esta disponible."}
        else:
            return {"message":"Codigo no encontrado."}
        
        return {"id":tempCode.id}