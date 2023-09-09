from create_app import db
from typing import Sequence
from datetime import datetime

import logging

logging.basicConfig(level=logging.DEBUG)
class ConversationMessageClass(db.Model):
    __tablename__ = 'conversation_message'
    
    #? STRUCTURE DB TABLE NOTIFICATION
    id               = db.Column(db.Integer,     primary_key=True)
    conversation_id  = db.Column(db.Integer,     db.ForeignKey('conversation.id'), nullable=False)
    message          = db.Column(db.Text,        default=None)
    archive_url      = db.Column(db.Text,        default=None)
    me               = db.Column(db.Integer,     default=0)
    status           = db.Column(db.Integer,     default=2)
    datetime         = db.Column(db.TIMESTAMP,   default=datetime.utcnow)
    datetime_update  = db.Column(db.TIMESTAMP,   nullable=True)
    
    @property
    def serialize(self):
        return{
            'id'              : self.id,
            'conversation_id' : self.conversation_id,
            'message'         : self.message,
            'archive_url'     : self.archive_url,
            'me'              : bool(self.me),
            'status'          : self.status,
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
        
        orderBy = getattr(ConversationMessageClass, 'id')
        if 'order_by' in filters:
            orderBy = getattr(ConversationMessageClass, filters['order_by'])
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
        conversation_messages: Sequence[ConversationMessageClass] = ConversationMessageClass.query.filter_by(**filters).all()
        conversation_messages = [conversation_message.serialize for conversation_message in conversation_messages]
        return conversation_messages
    
    @classmethod
    def getDataAllConversation(cls, id, name, phone):
        conversation_messages = ConversationMessageClass.query.filter_by(conversation_id=id).order_by(ConversationMessageClass.id.asc()).all()
        
        response = list()
        for message in conversation_messages:

            response.append({
                "id"            : message.id,
                "username"      : name if bool(message.me) else name,
                "message"       : message.message,
                "archive_url"   : message.archive_url,
                "me"            : bool(message.me),
                "datetime"      : message.datetime,
                "extra"         : None,
                "from"          : None if bool(message.me) else phone,
                "to"            : phone
            })
        return response
    
    @classmethod
    def putData(cls, data):
        db.session.commit()
        return data.serialize
    
    @classmethod
    def getDataFirstPut(cls, param):
        conversation_message = ConversationMessageClass.query.filter_by(id=param).first()
        return conversation_message
    
    @classmethod
    def post(cls, **cols):
        conversation_message = cls(**cols)
        db.session.add(conversation_message)
        db.session.commit()
        return conversation_message.serialize

    @classmethod
    def postData(cls, **cols):
        conversation_message = cls.post(**cols)
        return conversation_message