from flask import Flask
from flask_bootstrap import Bootstrap
from flask_moment import Moment
from flask_login import LoginManager
from config1 import config
from flask_security import Security
from flask_mongoengine import MongoEngine

bootstrap = Bootstrap()
moment = Moment()
db = MongoEngine()

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
    login_manager.login_view = 'main.login'

    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    return app