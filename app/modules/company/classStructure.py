from create_app import db
from typing import Sequence
from datetime import datetime
from . statusCodes import CodeID


class CompanyClass(db.Model):
    __tablename__ = 'company'

    #? STRUCTURE DB TABLE PLANS
    id              = db.Column(db.Integer,     primary_key=True)
    company_name    = db.Column(db.String(150), nullable=False)
    image_url       = db.Column(db.Text,        nullable=True)
    direction       = db.Column(db.Text,        nullable=True)
    satisfaction    = db.Column(db.DECIMAL(precision=None, scale=None, asdecimal=True),     default=0)
    status_id       = db.Column(db.Integer,     default=1)
    datetime        = db.Column(db.TIMESTAMP,   default=datetime.utcnow)
    datetime_update = db.Column(db.TIMESTAMP,   nullable=True)
 

    @property
    def serialize(self):
        return{
            'id'              : self.id,
            'company_name'    : self.company_name,
            'image_url'       : self.image_url,
            'direction'       : self.direction,
            'satisfaction'    : self.satisfaction,
            'status_id'       : CodeID(self.status_id),
            'datetime'        : self.datetime,
            'datetime_update' : self.datetime_update,
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
        
        orderBy = getattr(CompanyClass, 'id')
        if 'order_by' in filters:
            orderBy = getattr(CompanyClass, filters['order_by'])
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
    #* Metodo de consulta GET en company
    @classmethod
    def getData(cls, **filters):
        companys: Sequence[CompanyClass] = CompanyClass.query.filter_by(**filters).all()
        companys = [company.serialize for company in companys]
        return companys
    
   #* Metodo Indterno para el registro de compañias
    @classmethod
    def post(cls, **cols):
        company = cls(**cols)
        db.session.add(company)
        db.session.commit()
        return company.serialize

    @classmethod
    def getDataFirstUser(cls, param):
        company = CompanyClass.query.filter_by(user_id=param).first()
        return company.serialize
    
    @classmethod
    def getDataFirstPut(cls, param):
        company = CompanyClass.query.filter_by(id=param).first()
        return company
    
    @classmethod
    def putData(cls, data):
        db.session.commit()
        return data.serialize
    
    @classmethod
    def deletData(cls, data):
        db.session.delete(data)
        db.session.commit()
        company = CompanyClass.query.filter_by(id=data.id).first()
        if company is None:
            return{'message':'La compañia ha sido eliminada.'}
        else:
            return company.serialize