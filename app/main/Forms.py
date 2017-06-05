#  -*- coding: utf8 -*-
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, TextAreaField, SelectField, BooleanField
from wtforms.validators import DataRequired, Length
from flaskckeditor import CKEditor

import sys

# 处理中文编码的问题
default_encoding = 'utf-8'
if sys.getdefaultencoding() != default_encoding:
    reload(sys)

    sys.setdefaultencoding(default_encoding)


class PostForm(FlaskForm,CKEditor):
    title = StringField('标题',validators=[DataRequired()])
    abstract = TextAreaField('摘要',validators=[DataRequired()])
    tag = SelectField('标签', choices=[('code', '编程'), ('database', '数据库'),('essay', '随笔'), \
                                     ('tools', '工具'), ('net', '网络')], validators=[DataRequired()])
    body = TextAreaField("What's on your mind?",validators=[DataRequired()])
    submit = SubmitField('提交')

class AbooutMeForm(FlaskForm, CKEditor):
    about_me = TextAreaField('关于我', validators=[DataRequired()])
    submit = SubmitField('提交')

class LoginForm(FlaskForm):
    username = StringField('用户名', validators=[DataRequired(), Length(1, 64)])
    password = PasswordField('密码', validators=[DataRequired()])
    remember_me = BooleanField('remenber_me')
    submit = SubmitField('登录')

class CommentForm(FlaskForm):
    connect = StringField('联系方式')
    comment = TextAreaField('评论', validators=[DataRequired()])
    submit = SubmitField('提交')
