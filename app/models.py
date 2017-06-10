from datetime import datetime
from . import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_security import UserMixin, RoleMixin
from flask_login import current_user

class Users(db.Document, UserMixin):
    email = db.StringField(max_length=255)
    username = db.StringField()
    active = db.BooleanField(default=True)
    role = db.ReferenceField('Role')
    password_hash = db.StringField()
    confirm_at = db.DateTimeField()
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

    def can(self, permission):
        return current_user is not None and \
               (current_user.role.permission & permission) == permission

class Role(db.Document, RoleMixin):
    role_id = db.IntField()
    name = db.StringField(max_length=80, unique=True)
    permission = db.IntField()
    default = db.BooleanField(default=False)
    description = db.StringField(max_length=255)

    @staticmethod
    def insert_roles():
        roles = {
            'User':(Permissions.FOLLOW |
                    Permissions.COMMENT |
                    Permissions.WRITE_ARTICLES, True),
            'Moderator':(Permissions.FOLLOW |
                         Permissions.COMMENT |
                         Permissions.WRITE_ARTICLES |
                         Permissions.MODERATE_COMMENT, False),
            'Administrator':(Permissions.FOLLOW |
                         Permissions.COMMENT |
                         Permissions.WRITE_ARTICLES |
                         Permissions.MODERATE_COMMENT |
                         Permissions.ADMINISTER,False)
        }
        for r in roles:
            role = Role.objects(name=r).first()
            if role is None:
                role = Role(name=r)
            role.permission = roles[r][0]
            role.default = roles[r][1]
            c = ConfigId.objects(status='dev').first()
            role.role_id = c.role_id
            c.role_id += 1
            role.save()
            c.save()



class Permissions:
    FOLLOW = 0x01
    COMMENT = 0x02
    WRITE_ARTICLES = 0x04
    MODERATE_COMMENT = 0x08
    ADMINISTER = 0x80

class Posts(db.Document):
    head_pic = db.StringField()
    body_pic = db.StringField()
    title = db.StringField()
    body = db.StringField()
    abstract = db.StringField()
    tag = db.StringField()
    timestamp = db.DateTimeField(default=datetime.now())
    is_active = db.BooleanField(default=True)
    post_id = db.IntField()

    def __repr__(self):
        return '<Post %r>' % self.title


class ConfigId(db.Document):
    post_id = db.IntField()
    user_id = db.IntField()
    comment_id = db.IntField()
    role_id = db.IntField()
    status = db.StringField(default='dev')