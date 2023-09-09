from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
from flask_cors import CORS
import jwt
import os
from elasticsearch import Elasticsearch
load_dotenv()

# Crea la instancia de Flask
app = Flask(__name__)

# Configura la conexión a la base de datos
app.config['SQLALCHEMY_DATABASE_URI'] = f'mysql+mysqlconnector://{os.getenv("DB_USER")}:{os.getenv("DB_PASSWORD")}@{os.getenv("DB_HOST")}/{os.getenv("DB_NAME")}?charset=utf8mb4'
app.config['FLASK_DEBUG'] = False
app.config['SECRET_KEY'] = os.getenv("TOKEN_KEY")
CORS(app)
db = SQLAlchemy(app)
es = Elasticsearch(['http://elasticsearch:9200'])
