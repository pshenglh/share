import os
from mongoengine import connect

basedir = os.path.abspath(os.path.dirname(__file__))

class Config():
    BASE_DIR = basedir
    UPLOAD_FOLDER = 'app/static/pic'
    PIC_FOLDER = '/static/pic'
    ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])

    SECRET_KEY = 'anxious'
    UPLOAD_FOLDER = UPLOAD_FOLDER
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024

    MAIL_SERVER = 'smtp.qq.com'
    MAIL_PORT = 465
    MAIL_USER_TLS = True
    MAIL_USERNAME = '674799317@qq.com'
    MAIL_PASSWORD = 'pkqcdrfgqgglbahi'

class DevelopConfig(Config):
    MONGODB_SETTINGS = {
        'db': 'blog',
        'host': 'localhost',
        'port': 27017
    }
    DEFAULT_CONNECTION_NAME = connect('blog')
config = {
    'develop': DevelopConfig
}