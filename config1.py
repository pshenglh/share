import os

basedir = os.path.abspath(os.path.dirname(__file__))

class Config():
    BASE_DIR = basedir
    UPLOAD_FOLDER = 'app/static/pic'
    PIC_FOLDER = '/static/pic'
    ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])

    SECRET_KEY = 'anxious'
    UPLOAD_FOLDER = UPLOAD_FOLDER
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024

class DevelopConfig(Config):
    MONGOALCHEMY_DATABASE = 'blog'

config = {
    'develop': DevelopConfig
}