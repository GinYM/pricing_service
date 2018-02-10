from flask import Blueprint, render_template, request, json, url_for, redirect, session

from src.common.database import Database
from src.models.blogs.blog import Blog
import src.models.users.decorators as users_decorator
from src.models.blogs.post import Post
from src.models.users.user import User
import src.models.blogs.constants_post as PostConstant
import src.website_config as config
import src.models.blogs.constants as BlogConstant

blogs_blueprint = Blueprint('blogs', __name__)


@blogs_blueprint.route('/')
def index():
    if 'email' in session and session['email']:
        email = session['email']
    else:
        email = config.ADMIN_EMAIL


    user = User.find_by_email(email)
    if user is None:
        return render_template('users/login.jinja2')
    else:
        blogs = Blog.find_by_author_id(user._id)
        return render_template('blogs/user_blogs.jinja2', email=email, blogs=blogs)


@blogs_blueprint.route('/new',methods=['GET','POST'])
@users_decorator.require_login
def new_blog():
    if request.method == 'POST':
        user = User.find_by_email(session['email'])
        title = request.form['title']
        description = request.form['description']
        if request.form.get('secret'):
            user.new_blog(title=title, description=description, secret=1)
        else:
            user.new_blog(title=title,description=description,secret=0)
        return redirect(url_for('.index'))
    else:
        return render_template('blogs/new_blog.jinja2')


@blogs_blueprint.route('/edit_blogs')
@users_decorator.require_login
def edit_blogs():
    email = session['email']
    user = User.find_by_email(email)
    blogs = Blog.find_by_author_id(user._id)
    return render_template('blogs/edit_blogs.jinja2',email=email, blogs=blogs)


@blogs_blueprint.route('/edit_blog/<string:blog_id>',methods=['GET','POST'])
@users_decorator.require_login
def edit_blog(blog_id):
    blog = Blog.get_by_id(blog_id)
    if request.method == 'GET':
        return render_template('blogs/edit_blog.jinja2',blog=blog)
    else:
        blog.title = request.form['title']
        blog.description = request.form['description']
        if request.form.get('secret'):
            blog.secret = 1
        else:
            blog.secret = 0
        blog.save_to_mongo()
        return redirect(url_for('.index'))


@blogs_blueprint.route('/delete/<string:blog_id>',methods=['GET','POST'])
@users_decorator.require_login
def delete_blogs(blog_id):
    Database.remove(collection=BlogConstant.COLLECTION,query={'_id':blog_id})
    return redirect(url_for('.index'))



@blogs_blueprint.route('/posts/<string:blog_id>')
def posts(blog_id):
    blog = Blog.get_by_id(_id=blog_id)
    if blog is not None:
        posts = blog.get_post()
    else:
        posts = None
    return render_template('blogs/posts.jinja2',posts=posts,blog_title=blog.title if blog is not None else None, blog_id=blog_id)


@blogs_blueprint.route('/posts/new/<string:blog_id>', methods=['GET','POST'])
@users_decorator.require_login
def new_posts(blog_id):
    if request.method == 'GET':
        return render_template('blogs/new_post.jinja2', blog_id=blog_id)
    else:
        title = request.form['title']
        content = request.form['content']
        post = Post(blog_id=blog_id,title=title,content=content,author=session['email'])
        post.save_to_mongo()
        print("Here!")
        return redirect(url_for('.posts', blog_id=blog_id))


@blogs_blueprint.route('/posts/edit_posts/<string:blog_id>', methods=['GET','POST'])
@users_decorator.require_login
def edit_posts(blog_id):
    blog = Blog.get_by_id(_id=blog_id)
    if blog is not None:
        posts = blog.get_post()
    else:
        posts = None
    return render_template('blogs/edit_posts.jinja2',posts=posts,blog_title=blog.title if blog is not None else None, blog_id=blog_id)


@blogs_blueprint.route('/posts/edit/<string:post_id>', methods=['GET','POST'])
@users_decorator.require_login
def edit_post(post_id):
    post = Post.from_mongo(_id=post_id)
    if request.method == 'GET':
        return render_template('blogs/edit_post.jinja2',post=post,content = Post.reverse_replace_newline(post.content))
    else:
        post.title = request.form['title']
        post.content = Post.replace_newline(request.form['content'])
        post.save_to_mongo()
        return redirect(url_for('.posts',blog_id=post.blog_id))



@blogs_blueprint.route('/posts/delete/<string:post_id>', methods=['GET','POST'])
@users_decorator.require_login
def delete_post(post_id):
    post = Post.from_mongo(post_id)
    blog_id = post.blog_id
    Database.remove(collection=PostConstant.COLLECTION, query={'_id':post_id})
    return redirect(url_for('.edit_posts',blog_id=blog_id))

