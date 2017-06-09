import sqlite3
import os
from datetime import datetime
from app.models import Users, Posts, ConfigId

basedir = os.path.abspath(os.path.dirname(__file__))
sqlite_path = os.path.join(basedir, 'data.sqlite')
cx = sqlite3.connect(sqlite_path)

def insert_posts():
    cu = cx.cursor()
    cu.execute("SELECT head_pic, body_pic, title, body, abstract, tag, timestamp, is_active, id FROM posts ORDER BY id")
    post_items =  cu.fetchall()

    for post in post_items:
        dt = post[6].split('.')
        p = Posts(head_pic=str(post[0]), body_pic=str(post[1]), title=post[2], body=post[3],
             abstract=post[4], tag=post[5], timestamp=datetime.strptime(dt[0],'%Y-%m-%d %H:%M:%S'),
             is_active=bool(post[7]), post_id=int(post[8]))
        p.save()
    else:
        config_id = ConfigId(post_id=post[8], user_id=1)
        config_id.save()

def insert_user():
    cu = cx.cursor()
    cu.execute("SELECT username, password_hash, user_pic, about_me FROM admin")
    user_items = cu.fetchall()

    for user in user_items:
        u = Users(username=user[0], password_hash=user[1], user_pic='a', about_me=user[3])
        u.save()


if __name__ == '__main__':
    insert_posts()
    insert_user()


