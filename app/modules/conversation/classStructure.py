from create_app import db
from typing import Sequence
from datetime import datetime, timedelta
from .statusCodes import CodeID
from sqlalchemy import desc, func, or_
from modules.chatters.classStructure import ChattersClass
from modules.conversation_message.classStructure import ConversationMessageClass
import logging

logging.basicConfig(level=logging.DEBUG)

class ConversationClass(db.Model):
    __tablename__ = 'conversation'
    
    #? STRUCTURE DB TABLE NOTIFICATION
    id               = db.Column(db.Integer,     primary_key=True)
    bot_id           = db.Column(db.Integer,     nullable=False)
    chatter_id       = db.Column(db.Integer,     nullable=False)
    status_id        = db.Column(db.Integer,     default=1)
    datetime         = db.Column(db.TIMESTAMP,   default=(datetime.now() - timedelta(hours=4)).strftime("%Y-%m-%d %H:%M:%S"))
    datetime_update  = db.Column(db.TIMESTAMP,   nullable=True)
    
    @property
    def serialize(self):
        return{
            'id'              : self.id,
            'bot_id'          : self.bot_id,
            'chatter_id'      : self.chatter_id,
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
        
        orderBy = getattr(ConversationClass, 'id')
        if 'order_by' in filters:
            orderBy = getattr(ConversationClass, filters['order_by'])
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
        conversations: Sequence[ConversationClass] = ConversationClass.query.filter_by(**filters).all()
        conversations = [conversation.serialize for conversation in conversations]
        return conversations
    
    @classmethod
    def getDataAll(cls, chatter_id_list=None, **filters):
        conversations_query = cls.query
        if chatter_id_list is not None:
            conversations_query = conversations_query.filter(cls.chatter_id.in_(chatter_id_list))
        
        conversations = conversations_query.filter_by(**filters) \
            .order_by(
                desc(
                    func.coalesce(ConversationClass.datetime_update, ConversationClass.datetime - timedelta(hours=4))
                )
            ) \
            .all()          
            
        response = list()            
        for conversation in conversations:
            chatter = ChattersClass.getDataFirstID(conversation.chatter_id)
            name = chatter["phone"] if chatter["name"] is None else chatter["name"]
            phone = chatter["phone"]
            messages = ConversationMessageClass.getDataAllConversation(conversation.id, name, phone)
            
            response.append({
                "id"              : conversation.id,
                "chatter_id"      : chatter["id"],
                "chatterName"     : name,
                "conversation"    : messages,
                "chatterIconUrl"  : chatter["profile_img"],
                "status"          : CodeID(conversation.status_id),
                "datetime"        : conversation.datetime_update,
                "datetime_update" : conversation.datetime_update
            })
            
        return response
    
    @classmethod
    def putData(cls, data):
        db.session.commit()
        return data.serialize
    
    @classmethod
    def getDataFirstPut(cls, param):
        users = ConversationClass.query.filter_by(id=param).first()
        return users
    
    @classmethod
    def updateDatetime(cls, param):
        conversation = cls.getDataFirstPut(param)
        if conversation is not None:
            setattr(conversation, "datetime_update", (datetime.now() - timedelta(hours=4)).strftime("%Y-%m-%d %H:%M:%S"))
            conversation = cls.putData(conversation)
            
        return conversation
    
    @classmethod
    def post(cls, **cols):
        conversation = cls(**cols)
        db.session.add(conversation)
        db.session.commit()
        return conversation.serialize

    @classmethod
    def postData(cls, **cols):
        conversation = cls.post(**cols)
        return conversation
    
    @classmethod
    def getSearchFirst(cls, status, bot_id, chatter_id):
        conversation = ConversationClass.query.filter(
            ConversationClass.status_id.in_(status)
            ).filter(
                ConversationClass.bot_id == bot_id,
                ConversationClass.chatter_id == chatter_id
            ).first()
            
        if conversation is None:
            return dict()
        
        return conversation.serialize