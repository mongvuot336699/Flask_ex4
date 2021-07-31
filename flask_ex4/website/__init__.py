from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os

db = SQLAlchemy()
DB_NAME = 'database.db'

def creat_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'testing'
    app.config['SQL_ALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
    db.init_app(app)

    from .views import views

    app.register_blueprint(views, url_prefix='/')

    from .models import User 

    creat_db(app)

    return app 


def creat_db(app):
    if not os.path.exists('website' + DB_NAME):
        db.create_all(app=app)
        print('Created DB')

    