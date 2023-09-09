from create_app import db
from typing import Sequence
from datetime import datetime
from .statusCodes import CodeID


class NotificationClass(db.Model):
    __tablename__ = 'notification'
    
    #? STRUCTURE DB TABLE NOTIFICATION
    id               = db.Column(db.Integer,     primary_key=True)
    user_id          = db.Column(db.Integer,     db.ForeignKey('user.id'), nullable=False)
    title            = db.Column(db.Text,        nullable=False)
    body             = db.Column(db.Text,        default=True)
    url              = db.Column(db.Text,        nullable=True)
    operation_number = db.Column(db.String(64),  nullable=True)
    action_type      = db.Column(db.String(100), nullable=True)
    status_id        = db.Column(db.Integer,     default=2)
    datetime         = db.Column(db.TIMESTAMP,   default=datetime.utcnow)
    datetime_update  = db.Column(db.TIMESTAMP,   nullable=True)
    
    @property
    def serialize(self):
        return{
            'id'              : self.id,
            'user_id'         : self.user_id,
            'title'           : self.title,
            'body'            : self.body,
            'url'             : self.url,
            'operation_number': self.operation_number,
            'action_type'     : self.action_type,
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
        
        orderBy = getattr(NotificationClass, 'id')
        if 'order_by' in filters:
            orderBy = getattr(NotificationClass, filters['order_by'])
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
        
    @classmethod
    def getData(cls, **filters):
        notifications: Sequence[NotificationClass] = NotificationClass.query.filter_by(**filters).all()
        notifications = [notification.serialize for notification in notifications]
        return notifications
    
    @classmethod
    def putData(cls, data):
        db.session.commit()
        return data.serialize
    
    @classmethod
    def getDataFirstPut(cls, param):
        users = NotificationClass.query.filter_by(id=param).first()
        return users
