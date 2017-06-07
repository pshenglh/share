import sqlite3
import os
from datetime import datetime
from pymongo import *

basedir = os.path.abspath(os.path.dirname(__file__))
sqlite_path = os.path.join(basedir, 'data.sqlite')
cx = sqlite3.connect(sqlite_path)

client = MongoClient("localhost", 27017)
db = client.blog

def insert_posts():
    cu = cx.cursor()
    cu.execute("SELECT head_pic, body_pic, title, body, abstract, tag, timestamp, is_active, id FROM posts ORDER BY id")
    post_items =  cu.fetchall()
    posts = db.Posts

    for post in post_items:
        dt = post[6].split('.')
        p = {'head_pic':str(post[0]), 'body_pic':str(post[1]), 'title':post[2], 'body':post[3],
             'abstract':post[4], 'tag':post[5], 'timestamp':datetime.strptime(dt[0],'%Y-%m-%d %H:%M:%S'),
             'is_active':bool(post[7]), 'id':int(post[8])}
        posts.insert(p)

def insert_user():
    cu = cx.cursor()
    cu.execute("SELECT username, password_hash, user_pic, about_me FROM admin")
    user_items = cu.fetchall()
    users = db.Users

    for user in user_items:
        u = {'username':user[0], 'password_hash':user[1], 'user_pic':'a', 'about_me':user[3]}
        users.insert(u)

if __name__ == '__main__':
    insert_posts()
    insert_user()


