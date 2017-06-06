from datetime import datetime
from flask_login import UserMixin
from . import db
from werkzeug.security import generate_password_hash, check_password_hash

class Users(db.Document, UserMixin):
    username = db.StringField()
    password_hash = db.StringField()
    user_pic = db.StringField()
    about_me = db.StringField()

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)


class Posts(db.Document):
    head_pic = db.StringField()
    body_pic = db.StringField()
    title = db.StringField()
    body = db.StringField()
    abstract = db.StringField()
    tag = db.StringField()
    timestamp = db.DateTimeField(default=datetime.now())
    is_active = db.BoolField()
    id = db.IntField()

    def __repr__(self):
        return '<Post %r>' % self.title
