# import os
# from flask import Flask
# from flask_sqlalchemy import SQLAlchemy
# from api.config import Config

# db = SQLAlchemy()

# def create_app(config_class=Config):
#   basedir = os.path.abspath(os.path.dirname(__file__))

#   app = Flask(__name__)

#   db.init_app(app)

#   return app
from flask import Flask
from flask_restful import Api 
from flask_sqlalchemy import SQLAlchemy 

app = Flask(__name__)
app.debug=True 
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'

api = Api(app)
db = SQLAlchemy(app)

from api.resources.item import Item

api.add_resource(Item, '/item/<int:item_id>')