#  -*- coding: utf8 -*-
import unittest
from flask import current_app, url_for
from app import create_app, db
from app.models import Admin, Post, Comment
import os


class BasicsTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app('test')
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()
        self.client = self.app.test_client()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_app_exists(self):
        self.assertFalse(current_app is None)

    def test_app_is_testing(self):
        self.assertTrue(current_app.config['TESTING'])

    def test_index(self):
        response = self.client.get(url_for('main.index'))
        self.assertTrue('文章' in response.data)

    def test_login_logout(self):
        admin = Admin()
        admin.username = 'test'
        admin.password = 'test'
        db.session.add(admin)
        db.session.commit()
        user = Admin.query.filter_by(id=1).first()
        self.assertTrue('test'==user.username)
        self.assertTrue(user.verify_password('test'))

        response = self.client.post(url_for('main.login'), data=dict(
            username='test',
            password='test',
        ), follow_redirects=True)
        self.assertTrue('退出' in response.data)
        self.assertTrue('文章' in response.data)

        response = self.client.get(url_for('main.logout'), follow_redirects=True)
        self.assertTrue('登录' in response.data)
        self.assertTrue('文章' in response.data)

    def test_post(self):
        #添加用户并登录获取权限admin = Admin()
        admin = Admin()
        admin.username = 'test'
        admin.password = 'test'
        db.session.add(admin)
        db.session.commit()
        self.client.post(url_for('main.login'), data=dict(
            username='test',
            password='test'
        ), follow_redirects=True)

        title_test = 'title_test'
        abstract_test = 'abstract_test'
        tag_test = 'code'
        body_test = 'body_test '

        #写博客
        response = self.client.get(url_for('main.write_post'), follow_redirects=True)
        self.assertTrue(response.status_code==200)
        self.assertTrue('提交' in response.data)
        response = self.client.post(url_for('main.write_post'), data=dict(
            title=title_test,
            abstract = abstract_test,
            tag=tag_test,
            body=body_test
        ), follow_redirects=True)
        self.assertTrue(response.status_code==200)
        p = Post.query.filter_by(title=title_test).first()
        self.assertTrue(p.abstract==abstract_test)
        self.assertTrue(p.tag==u'code-编程')
        self.assertTrue(p.body==body_test)

        #修改博客
        response = self.client.get(url_for('main.edit_post', id=p.id), follow_redirects=True)
        self.assertTrue(title_test in response.data)
        self.assertTrue(abstract_test in response.data)
        self.assertTrue('编程' in response.data)
        self.assertTrue(body_test in response.data)

        m_title_test = 'm_title_test'
        m_abstract_test = 'm_abstract_test'
        m_tag_test = 'net'
        m_body_test = 'm_body_test '
        response = self.client.post(url_for('main.edit_post', id=p.id), data=dict(
            title=m_title_test,
            abstract=m_abstract_test,
            tag=m_tag_test,
            body=m_body_test
        ), follow_redirects=True)
        self.assertTrue(m_title_test in response.data)
        p1 = Post.query.filter_by(id=p.id).first()
        self.assertTrue(p1.title==m_title_test)
        self.assertTrue(p1.abstract==m_abstract_test)
        self.assertTrue(p1.tag==u'net-网络')
        self.assertTrue(p1.body==m_body_test)

        # 查看博客
        # 评论功能
        comment = 'comment_test'
        connection = '123@456.com'
        self.client.post(url_for('main.post', id=p.id), data=dict(
            comment=comment,
            connect=connection
        ), follow_redirects=True)
        comments = Comment.query.filter_by(post_id=p.id).first()
        self.assertTrue(comments.connection == connection)
        self.assertTrue(comments.body == comment)
        response = self.client.get(url_for('main.post', id=p.id))
        self.assertTrue(response.status_code==200)
        self.assertTrue(p.title in response.data)
        self.assertTrue(comments.body in response.data)

        #删除评论
        self.client.post(url_for('main.delete_comment', id=comments.id))
        comment_del = Comment.query.filter_by(id=comments.id).first()
        self.assertIsNone(comment_del)

        #删除博客
        self.client.post(url_for('main.delete_post', id=p.id))
        p2 = Post.query.filter_by(id=p.id).first()
        self.assertFalse(p2.is_active)

    def test_about_me(self):
        admin = Admin()
        admin.username = 'test'
        admin.password = 'test'
        admin.about_me = 'about_me_test'
        db.session.add(admin)
        db.session.commit()
        self.client.post(url_for('main.login'), data=dict(
            username='test',
            password='test'
        ), follow_redirects=True)

        response = self.client.get(url_for('main.about_me'), follow_redirects=True)
        self.assertTrue('about_me_test' in response.data)

        response = self.client.get(url_for('main.edit_about_me'), follow_redirects=True)
        self.assertTrue('about_me_test' in response.data)

        response = self.client.post(url_for('main.edit_about_me'), data=dict(
            about_me='m_about_me_test'
        ), follow_redirects=True)
        self.assertTrue('m_about_me_test' in response.data)

    def test_classify(self):
        response = self.client.get(url_for('main.index'))
        self.assertTrue('<h3>所有文章</h3>' in response.data)
        response = self.client.get(url_for('main.code'))
        self.assertTrue('<h3>编程</h3>' in response.data)
        response = self.client.get(url_for('main.net'))
        self.assertTrue('<h3>网络</h3>' in response.data)
        response = self.client.get(url_for('main.tool'))
        self.assertTrue('<h3>工具</h3>' in response.data)
        response = self.client.get(url_for('main.database'))
        self.assertTrue('<h3>数据库</h3>' in response.data)
        response = self.client.get(url_for('main.essay'))
        self.assertTrue('<h3>随笔</h3>' in response.data)

    def test_pic_upload(self):
        #登录获取权限以供后续测试
        admin = Admin()
        admin.username = 'test'
        admin.password = 'test'
        db.session.add(admin)
        db.session.commit()
        self.client.post(url_for('main.login'), data=dict(
            username='test',
            password='test'
        ), follow_redirects=True)

        title_test = 'title_test'
        abstract_test = 'abstract_test'
        tag_test = 'code'
        body_test = 'body_test '

        # 插入一个文章以供后续测试
        response = self.client.post(url_for('main.write_post'), data=dict(
            title=title_test,
            abstract=abstract_test,
            tag=tag_test,
            body=body_test
        ), follow_redirects=True)
        self.assertTrue(response.status_code == 200)
        p = Post.query.filter_by(title=title_test).first()
        self.assertTrue(p.abstract == abstract_test)
        self.assertTrue(p.tag == u'code-编程')
        self.assertTrue(p.body == body_test)


        #上传主题图片
        file = open('test.txt', 'w+')
        file.write('111111')
        response = self.client.post(url_for('main.uploaded_file', id=p.id), data=dict(
            file=file
        ), follow_redirects=True)
        file.close()
        self.assertTrue(os.path.join(current_app.config['PIC_FOLDER'], 'test.txt') in response.data)
        self.assertTrue(response.status_code==200)
        self.assertTrue(os.path.exists(os.path.join(current_app.config['BASE_DIR'],
                                current_app.config['UPLOAD_FOLDER'], 'test.txt')))
        self.assertTrue(p.head_pic==os.path.join(current_app.config['PIC_FOLDER'], 'test.txt'))
        os.remove('test.txt')

        #修改主题图片
        file = open('test1.txt', 'w+')
        file.write('222222')
        response = self.client.post(url_for('main.uploaded_file', id=p.id), data=dict(
            file=file
        ), follow_redirects=True)
        file.close()
        self.assertTrue(response.status_code == 200)
        self.assertTrue(os.path.join(current_app.config['PIC_FOLDER'], 'test1.txt') in response.data)
        self.assertFalse(os.path.exists(os.path.join(current_app.config['BASE_DIR'],
                                current_app.config['UPLOAD_FOLDER'], 'test.txt')))
        self.assertTrue(os.path.exists(os.path.join(current_app.config['BASE_DIR'],
                                     current_app.config['UPLOAD_FOLDER'], 'test1.txt')))
        self.assertTrue(p.head_pic == os.path.join(current_app.config['PIC_FOLDER'], 'test1.txt'))
        os.remove('test1.txt')

        #测试上传文章内容图片
        file = open('test.txt', 'w+')
        file.write('111111')
        response = self.client.post(url_for('main.post_pic', id=p.id), data=dict(
            file=file
        ), follow_redirects=True)
        file.close()
        self.assertTrue(response.status_code == 200)
        self.assertTrue(os.path.join(current_app.config['PIC_FOLDER'], '0'+str(p.id), 'test.txt') in response.data)
        self.assertTrue(os.path.exists(os.path.join(current_app.config['BASE_DIR'], current_app.config['UPLOAD_FOLDER'],
                                         '0'+str(p.id), 'test.txt')))
        self.assertTrue(p.body_pic == os.path.join(current_app.config['PIC_FOLDER'], '0'+str(p.id), 'test.txt'))
        os.remove('test.txt')

        file = open('test1.txt', 'w+')
        file.write('2222222')
        response = self.client.post(url_for('main.post_pic', id=p.id), data=dict(
            file=file
        ), follow_redirects=True)
        file.close()
        self.assertTrue(response.status_code == 200)
        self.assertTrue(os.path.join(current_app.config['PIC_FOLDER'], '0' + str(p.id), 'test1.txt') in response.data)
        self.assertTrue(os.path.exists(os.path.join(current_app.config['BASE_DIR'],
                                         current_app.config['UPLOAD_FOLDER'], '0' + str(p.id), 'test1.txt')))
        self.assertTrue(p.body_pic == os.path.join(current_app.config['PIC_FOLDER'], '0' + str(p.id), 'test.txt')+
                        '|'+os.path.join(current_app.config['PIC_FOLDER'], '0' + str(p.id), 'test1.txt'))
        os.remove('test1.txt')

        #删除文章后对相关图片的删除
        response = self.client.get(url_for('main.delete_post_fully', id=p.id), follow_redirects=True)
        self.assertTrue(response.status_code==200)
        self.assertFalse(os.path.exists(os.path.join(current_app.config['BASE_DIR'],
                         current_app.config['UPLOAD_FOLDER'], os.path.basename(p.head_pic))))
        self.assertFalse(os.path.exists(os.path.join(current_app.config['BASE_DIR'],
                                                     current_app.config['UPLOAD_FOLDER'], '0'+str(p.id))))