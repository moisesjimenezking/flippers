from create_app import db
from typing import Sequence
from datetime import datetime

class PlansClass(db.Model):
    __tablename__ = 'plans'
    
    #? STRUCTURE DB TABLE PLANS
    id              = db.Column(db.Integer,                       primary_key=True)
    name            = db.Column(db.String(120),                   nullable=False)
    code            = db.Column(db.String(64),                    nullable=False)
    amount          = db.Column(db.DECIMAL(precision=13, scale=2),nullable=False, default=0)
    description     = db.Column(db.Text,                          nullable=True)
    status_id       = db.Column(db.Integer,                       default=1)
    datetime        = db.Column(db.TIMESTAMP,                     default=datetime.utcnow)
    datetime_update = db.Column(db.TIMESTAMP,                     nullable=True)
 
    # status = db.relationship(UserStatus, lazy='select')
    
    @property
    def serialize(self):
        return{
            'id'              : self.id,
            'name'            : self.name,
            'code'            : self.code,
            'amount'          : self.amount,
            'description'     : self.description,
            'status_id'       : self.status_id,
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
        
        orderBy = getattr(PlansClass, 'id')
        if 'order_by' in filters:
            orderBy = getattr(PlansClass, filters['order_by'])
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
    def getData(cls, **filters):
        plans: Sequence[PlansClass] = PlansClass.query.filter_by(**filters).all()
        plans = [plan.serialize for plan in plans]
        return plans