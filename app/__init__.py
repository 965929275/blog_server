# encoding:utf8
from flask import Flask
from config import config
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail


db = SQLAlchemy()
mail = Mail()

def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])

    db.init_app(app)
    mail.init_app(app)

    # 注册auth蓝本
    from .auth import auth
    app.register_blueprint(auth,url_prefix='/auth')

    # 注册main
    from .main import main
    app.register_blueprint(main, url_prefix='/main')

    from .api import api
    app.register_blueprint(api,url_prefix='/hello')

    return app