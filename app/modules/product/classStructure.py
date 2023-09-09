from create_app import db, es
from typing import Sequence
from datetime import datetime
from sqlalchemy import or_
from gensim.models import FastText
from .statusCodes import CodeID


# from modules.subscriptions.classStructure import SubscriptionsClass
# from modules.boots.classStructure import BootsClass
import logging

logging.basicConfig(level=logging.DEBUG)

class ProductClass(db.Model):
    __tablename__ = 'products'
    
    index = "products"
    
    #? STRUCTURE DB TABLE USER
    id              = db.Column(db.Integer, primary_key=True)
    user_id         = db.Column(db.Integer, nullable=False)
    bot_id          = db.Column(db.Integer, nullable=True)
    name            = db.Column(db.Text,    nullable=False)
    code            = db.Column(db.String(60), nullable=True)
    description     = db.Column(db.Text, nullable=True)
    price           = db.Column(db.DECIMAL(precision=13, scale=2),nullable=False, default=0)
    discount        = db.Column(db.Text, nullable=True)
    currency_code   = db.Column(db.String(10), nullable=False, default="Bs")
    quantity        = db.Column(db.Integer, default=0)
    footer          = db.Column(db.Text, nullable=True)
    url             = db.Column(db.Text, nullable=True)
    status_id       = db.Column(db.Integer, default=1)
    datetime        = db.Column(db.TIMESTAMP, default=datetime.utcnow)
    datetime_update = db.Column(db.TIMESTAMP, nullable=True)
 
    # status = db.relationship(UserStatus, lazy='select')
#     subscriptions = db.relationship(SubscriptionsClass, lazy='select', uselist=False)
#     bots = db.relationship(BootsClass, lazy='select', uselist=False)
# #  primaryjoin='and_(BootsClass.status_id==2)'
   
    @property
    def serialize(self):
        doc = {
            'bot_id': self.bot_id,
            'name': self.name
        }
        
        es.index(index='products', id=self.id, body=doc)
        
        return{
            'id'              : self.id,
            'user_id'         : self.user_id,
            'bot_id'          : self.bot_id,
            'name'            : self.name,
            'code'            : self.code,
            'description'     : self.description,
            'price'           : self.price,
            'discount'        : float(self.discount),
            'currency_code'   : self.currency_code,
            'quantity'        : self.quantity,
            'footer'          : self.footer,
            'url'             : self.url,
            'status_id'       : CodeID(self.status_id),
            'datetime'        : self.datetime,
            'datetime_update' : self.datetime_update,
            
            # * Llaves foraneas
            # 'subscriptions': None if self.subscriptions is None else self.subscriptions.serialize,
            # 'bots': None if self.bots is None else self.bots.serialize,
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
        
        orderBy = getattr(ProductClass, 'id')
        if 'order_by' in filters:
            orderBy = getattr(ProductClass, filters['order_by'])
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
        users = ProductClass.query.filter_by(id=param).first()
        return users
     
    #* Metodo de consulta GET en users permite filtros estandars y exactos
    #* En caso de que la coincidencia sea 1 se retorna un obj
    #* En caso de que la coincidencia sea mayor a 1 se retorna un array de obj
    @classmethod
    def getData(cls, **filters):
        products: Sequence[ProductClass] = ProductClass.query.filter_by(**filters).all()
        response = []
        
        indice_existe = es.indices.exists(index=cls.index)
        if indice_existe == False:
            es.indices.create(index=cls.index)
            
        for product in products:
            aux = product.serialize
            
            # fasttext_model = FastText.load_model("/app/config/modelsFastText/products_{}.model".format(aux["user_id"]))
            # product_vector = fasttext_model.get_sentence_vector(aux["name"])
                
            response.append(aux)
            
            doc = {
                'bot_id': aux["bot_id"],
                'name': aux['name'],
                # 'vector': product_vector.tolist()
            }

            documentExiste = es.exists(index=cls.index, id=aux["id"])
            if documentExiste:
                es.update(index=cls.index, id=aux["id"], body={'doc': doc})
            else:
                es.index(index=cls.index, id=aux["id"], body=doc)

        return response
    
    #* Metodo de actualizacion de usuarios
    #* Es requerido el ID del usuario
    def putData(data):
        db.session.commit()
        return data.serialize
    
    def deletData(data):
        db.session.delete(data)
        db.session.commit()
        product = ProductClass.query.filter_by(id=data.id).first()
        if product is None:
            return{'message':'El producto ha sido eliminado.'}
        else:
            return product.serialize
    
    #* Metodo Indterno para el registro de usuarios
    @classmethod
    def post(cls, **cols):
        users = cls(**cols)
        db.session.add(users)
        db.session.commit()
        users = cls.getData(**cols)
        
        indice_existe = es.indices.exists(index=cls.index)
        if indice_existe == False:
            es.indices.create(index=cls.index)
            
        doc = {
            'bot_id': users[0]["bot_id"],
            'name': users[0]['name']
        }

        es.index(index=cls.index, id=users[0]["id"], body=doc)

        return users

    #* Metodo Externo para el registro de usuarios 
    #* Este metodo comprueba la existencia de un usuario en la base de datos
    #* En caso de existir no se procede con el registro
    @classmethod
    def postData(cls, **cols):
        if 'name' in cols and 'user_id' in cols:
            username = ProductClass.query.filter_by(name=cols["name"], user_id=cols["user_id"]).first()
            if username is not None:
                return{'message':'El nombre del producto ya se encuentra registrado.'}
            
        users = cls.post(**cols)
        return users
    
    @classmethod
    def getDataLike(cls, bot_id, product):
        users: Sequence[ProductClass] = ProductClass.query.filter_by(bot_id=bot_id).filter(or_(ProductClass.name == product, ProductClass.name.like(f'%{product}%'))).all()
        users = [user.serialize for user in users]
        return users
    
    @classmethod
    def getElastic(cls, bot_id, name):
        listData = list()
        search_result = es.search(
            index='products', body={
                "query": {
                    "fuzzy": {
                        "name": {
                            "value": name,
                            "fuzziness": "2"
                        }
                    }
                }
            }
        )
        
        listData.extend(search_result["hits"]["hits"])
        search_result = es.search(
            index='products',
            body={
                "query": {
                    "match": {
                        "name": name
                    }
                }
            }
        )

        listData.extend(search_result["hits"]["hits"])        
        search_result = es.search(
            index='products',
            body={
                "query": {
                    "query_string": {
                        "query": f"name:*{name}*"
                    }
                }
            }
        )

        listData.extend(search_result["hits"]["hits"])
        
        proccesind = list()
        response = list()

        for x in range(len(listData)):
            if listData[x]["_id"] not in proccesind:
                proccesind.append(listData[x]["_id"])

                users = ProductClass.query.filter_by(id=listData[x]["_id"], bot_id=bot_id).first()
                if users is not None:
                    users = users.serialize
                    response.append(users)
                    
                
                
        return response