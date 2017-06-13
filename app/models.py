from datetime import datetime
from . import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_security import UserMixin, RoleMixin
from flask_login import current_user
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from flask import current_app


class Users(db.Document, UserMixin):
    user_id = db.IntField()
    email = db.StringField(unique=True, max_length=255)
    username = db.StringField(unique=True)
    active = db.BooleanField(default=True)
    role = db.ReferenceField('Role')
    password_hash = db.StringField()
    confirm_at = db.DateTimeField()
    user_pic = db.StringField()
    description = db.StringField()
    confirmed = db.BooleanField(default=False)

    def __init__(self, **kwargs):
        super(Users, self).__init__(**kwargs)
        if self.role == None:
            print 1
            r = Role.objects(name='User').first()
            self.role = r

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

    def generation_confirmaton_token(self, expiration=3600):
        s = Serializer(current_app.config['SECRET_KEY'], expiration)
        return s.dumps({'confirm': self.user_id})

    def confirm(self, token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token)
        except:
            return False
        if data.get('confirm') != self.user_id:
            return False
        self.confirmed = True
        self.save()
        return True

    def follow(self, user_id):
        followers_id = [r.follower.user_id for r in Relationship.objects(followed=self).all()]
        if user_id not in followers_id:
            follower = Users.objects(user_id=user_id).first()
            r = Relationship(followed=self, follower=follower)
            r.save()
        else:
            return 'followed'


class Role(db.Document, RoleMixin):
    role_id = db.IntField()
    name = db.StringField(max_length=80, unique=True)
    permission = db.IntField()
    default = db.BooleanField(default=False)
    description = db.StringField(max_length=255)

    @staticmethod
    def insert_roles():
        roles = {
            'User': (Permissions.FOLLOW |
                     Permissions.COMMENT |
                     Permissions.WRITE_ARTICLES, True),
            'Moderator': (Permissions.FOLLOW |
                          Permissions.COMMENT |
                          Permissions.WRITE_ARTICLES |
                          Permissions.MODERATE_COMMENT, False),
            'Administrator': (Permissions.FOLLOW |
                              Permissions.COMMENT |
                              Permissions.WRITE_ARTICLES |
                              Permissions.MODERATE_COMMENT |
                              Permissions.ADMINISTER, False)
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


class Relationship(db.Document):
    followed = db.ReferenceField('Users')
    follower = db.ReferenceField('Users')


class Posts(db.Document):
    head_pic = db.StringField()
    body_pic = db.StringField()
    title = db.StringField()
    author = db.ReferenceField('Users')
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