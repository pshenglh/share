from . import api
from ..models import Posts, Permissions
from flask import jsonify, request, g, url_for
from .decorators import permission_required
from .errors import forbidden

@api.route('/posts/')
def get_posts():
    posts = Posts.objects
    return jsonify({'posts': [post.to_json() for post in posts]})

@api.route('/post/<int:id>')
def get_post(id):
    post = Posts.objects(post_id=id).first()
    return jsonify(post.to_json())

@api.route('/post/', methods=['POST'])
@permission_required(Permissions.WRITE_ARTICLES)
def new_post():
    post = Posts.from_json(request.json)
    post.author = g.current_user
    post.save()
    return jsonify(post.to_json(), 201,
                   {'Location': url_for('api.get_post', id=post.post_id, _external=True)})

@api.route('/post/<int:id>', methods=['PUT'])
@permission_required(Permissions.WRITE_ARTICLES)
def edit_post(id):
    post = Posts.objects(post_id=id).first()
    if g.current_user != post.author and \
        not g.current_user.can(Permissions.ADMINISTER):
        return forbidden('No permission')
    post.body = request.json.get('body')
    post.save()
    return jsonify(post.to_json())
