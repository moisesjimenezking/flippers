from create_app import db
from typing import Sequence
from datetime import datetime
from modules.user.classStructure import UserClass
from modules.company.classStructure import CompanyClass
from sqlalchemy import or_
import logging

logging.basicConfig(level=logging.DEBUG)
class ChattersClass(db.Model):
    __tablename__ = 'chatters'

    #? STRUCTURE DB TABLE PLANS
    id              = db.Column(db.Integer,     primary_key=True)
    user_id         = db.Column(db.Integer,     nullable=False)
    name            = db.Column(db.Text,        nullable=True)
    profile_img     = db.Column(db.Text,        nullable=True)
    phone           = db.Column(db.Text(20),    nullable=False)
    last_direction  = db.Column(db.Integer,     nullable=True)
    quantity_shoping= db.Column(db.Integer,     nullable=True)
    satisfaction    = db.Column(db.Text(10),    nullable=True)
    list_wait       = db.Column(db.Boolean,    default=0)
    list_black      = db.Column(db.Boolean,    default=0)
    list_attention  = db.Column(db.Boolean,    default=0)
    status_id       = db.Column(db.Integer,     default=2)
    datetime        = db.Column(db.TIMESTAMP,   default=datetime.utcnow)
    datetime_update = db.Column(db.TIMESTAMP,   nullable=True)
 
    # order = db.relationship(OrdersClass, lazy='select', uselist=False)
    # product = db.relationship(ProductClass, lazy='select', uselist=False)
    
    @property
    def serialize(self):
        return{
            'id'                : self.id,
            'user_id'           : self.user_id,
            'name'              : self.name,
            'profile_img'       : self.profile_img,
            'phone'             : self.phone,
            'last_direction'    : self.last_direction,
            'quantity_shoping'  : self.quantity_shoping,
            'satisfaction'      : self.satisfaction,
            'list_wait'         : self.list_wait,
            'list_black'        : self.list_black,
            'list_attention'    : self.list_attention,
            'status_id'         : self.status_id,
            'datetime'          : self.datetime,
            'datetime_update'   : self.datetime_update,
            
            # * Llaves foraneas
            # 'order': None if self.order is None else self.order.serialize,
            # 'product': None if self.product is None else self.product.serialize,
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
        
        orderBy = getattr(ChattersClass, 'id')
        if 'order_by' in filters:
            orderBy = getattr(ChattersClass, filters['order_by'])
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
    def getDataTime(cls, datetime, user):
        sales = ChattersClass.query.filter_by(user_id=user).filter(ChattersClass.datetime < datetime).order_by(ChattersClass.id.desc()).all()
        sales = [sale.serialize for sale in sales]
        return sales
    
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
        
        sales: Sequence[ChattersClass] = ChattersClass.query.filter_by(**filters).\
            order_by(desc(orderBy) if typeOrderBy else orderBy).\
            offset(page).limit(limit).all()
            
        sales = [sale.serialize for sale in sales]
        return sales
    
     #* Metodo Indterno para el registro de usuarios
    @classmethod
    def post(cls, **cols):
        sales = cls(**cols)
        db.session.add(sales)
        db.session.commit()
        sales = cls.getData(**cols)
        return sales

    #* Metodo Externo para el registro de usuarios 
    #* Este metodo comprueba la existencia de un usuario en la base de datos
    #* En caso de existir no se procede con el registro
    @classmethod
    def postData(cls, **cols):
        if ChattersClass.query.filter_by(phone=cols["phone"], user_id=cols["user_id"]).first() is not None:
            return{'message':'El chatters ya se encuentra registrado para este usuario'}

        sales = cls.post(**cols)
        return sales
    
    @classmethod
    def getDataFirstID(cls, id):
        chatter = ChattersClass.query.filter_by(id=id).first()
        return chatter.serialize
    
    @classmethod
    def getDataFirstIdPut(cls, id):
        chatter = ChattersClass.query.filter_by(id=id).first()
        return chatter

    @classmethod
    def getDataFirst(cls, user_id, phone):
        chatter = ChattersClass.query.filter_by(user_id=user_id, phone=phone).first()
        return chatter
    
    @classmethod
    def getChattersFirst(cls, **params):
        chatters = ChattersClass.query.filter_by(**params).first()
        
        if chatters is None:
            return dict()
        
        return chatters.serialize
    
    @classmethod
    def getChattersLike(cls, search_term):
        chatters = cls.query.filter(
            or_(
                cls.name.ilike(f"%{search_term}%"),
                cls.phone.ilike(f"%{search_term}%")
            )
        ).all()
        
        if not chatters:
            return []
        
        response = []
        for chatter in chatters:
            response.append(chatter.serialize["id"])
            
        return response
    
    @classmethod
    def getDataFirstPut(cls, phone):
        users = ChattersClass.query.filter_by(phone=phone).first()
        return users
    
    @classmethod
    def putData(cls, data):
        setattr(data, "datetime_update", datetime.now())
        db.session.commit()
        return data.serialize
    
    @classmethod
    def satisfactionData(cls, user_id):
        chatters = ChattersClass.query.filter_by(user_id=user_id).all()
        if chatters is not None:
            chattersSatisfaction = 0
            satisfactionAll = 0
            media = 0
            for chatter in chatters:
                if chatter.satisfaction is not None and float(chatter.satisfaction) > 0:
                    chattersSatisfaction += 1
                    satisfactionAll += float(chatter.satisfaction)
                    
            if chattersSatisfaction > 0 and satisfactionAll > 0:
                media = round(float(satisfactionAll)/int(chattersSatisfaction), 2)
                
            user = UserClass.getDataFirst(user_id)
            company = CompanyClass.getDataFirstPut(user["company_id"])
            setattr(company, "satisfaction", media)
            company = CompanyClass.putData(company)
            
            return True
        
        return False
    
    @classmethod
    def getDataApp(cls, **filters):
        conditions = []
        if 'name_chatters' in filters:
            conditions.append(ChattersClass.name.like(f"%{filters['name_chatters']}%"))

        if 'quantity_shoping' in filters:
            conditions.append(ChattersClass.quantity_shoping >= filters['quantity_shoping'])


        # Construir la consulta
        if conditions:
            sales = ChattersClass.query.filter(*conditions).order_by(ChattersClass.id.desc()).all()
        else:
            sales = ChattersClass.query.filter_by(**filters).order_by(ChattersClass.id.desc()).all()


        # sales: Sequence[ChattersClass] = ChattersClass.query.filter_by(**filters).order_by(ChattersClass.id.desc()).all()
        response = list()
        for sale in sales:
            aux = {
                'id'                : sale.id,
                'name'              : sale.name,
                'profile_img'       : sale.profile_img,
                'phone'             : sale.phone,
                'last_direction'    : sale.last_direction,
                'quantity_shoping'  : sale.quantity_shoping if sale.quantity_shoping is not None else 0,
                'satisfaction'      : sale.satisfaction,
                'list_wait'        : sale.list_wait,
                'list_black'        : sale.list_black,
                'list_attention'    : sale.list_attention,
            }
            
            response.append(aux)
            
        return response