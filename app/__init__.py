from flask import Flask
from flask_bootstrap import Bootstrap
from flask_moment import Moment
from flask_mongoalchemy import MongoAlchemy
from flask_login import LoginManager
from config1 import config


bootstrap = Bootstrap()
moment = Moment()
db = MongoAlchemy()

login_manager = LoginManager()
login_manager.session_protection = 'strong'
login_manager.login_view = 'auth.login'


def create_app(config_name='develop'):
    app = Flask(__name__)
    app.config.from_object(config[config_name])

    bootstrap.init_app(app)
    moment.init_app(app)
    db.init_app(app)
    login_manager.init_app(app)

    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    return app