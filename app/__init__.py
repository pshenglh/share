from flask import Flask
from flask_bootstrap import Bootstrap
from flask_moment import Moment
from config1 import config
from flask_login import LoginManager
from flask_mongoengine import MongoEngine

bootstrap = Bootstrap()
moment = Moment()
db = MongoEngine()

login_manager = LoginManager()
login_manager.session_protection = 'strong'
login_manager.login_view = 'main.login'


def create_app(config_name='develop'):
    from .models import Users, Role
    app = Flask(__name__)
    app.config.from_object(config[config_name])

    bootstrap.init_app(app)
    moment.init_app(app)
    db.init_app(app)
    login_manager.init_app(app)

    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    return app