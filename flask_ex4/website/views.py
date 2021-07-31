from flask import Blueprint , render_template, request, flash, redirect , session , g
from flask.helpers import url_for
from werkzeug.security import check_password_hash, generate_password_hash 
from werkzeug.exceptions import abort
import functools

from . import db 
from .models import User , Post

views = Blueprint('views',__name__)



@views.route('/login', methods = ['GET','POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        user = User.query.filter_by(username = username).first()
        if user:
            if check_password_hash(user.password,password):
                flash('Login suceed')
                session.clear()
                session['user_id'] = user.id
                return redirect(url_for('views.index')) 

        flash('User or pass not correct !')
    return render_template('login.html')


@views.route('/register', methods = ['GET','POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        check_user = User.query.filter_by(username = username).first()
        if check_user:
            flash('Username have been exists', category='error')
        else:
            user = User(username = username, password= generate_password_hash(password))
            db.session.add(user)
            db.session.commit()
            flash('User creat suceeds')
            return redirect(url_for('views.login'))

    return render_template('register.html')

@views.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('views.login'))

@views.before_app_request
def load_logged_in_user():
    user_id = session.get('user_id')

    if user_id is None:
        g.user = None
    else:
        user = User.query.filter_by(id = user_id).first()
        g.user = user

def login_required(view):
    @functools.wraps(view)
    def wrapped_view(*args,**kwargs):
        if g.user is None:
            return redirect(url_for('views.login'))

        return view(*args,**kwargs)

    return wrapped_view


#---------------------BLOG==================================#
@views.route('/')
def index():
    posts = Post.query.all()
    return render_template('test.html', posts=posts)
    

@views.route('/create', methods=('GET', 'POST'))
@login_required
def create():
    if request.method == 'POST':
        title = request.form['title']
        body = request.form['body']
        error = None

        if not title:
            error = 'Title is required.'

        if error is not None:
            flash(error)
        else:
            user = User.query.get(session['user_id'])
            data = Post(title = title, body = body, author_id = user.id)
            db.session.add(data)
            db.session.commit()
            return redirect(url_for('views.index'))

    return render_template('creat.html')


def get_post(id, check_author=True):
    post = Post.query.filter_by(id=id).first_or_404()

    if post is None:
        abort(404, f"Post id {id} doesn't exist.")

    if check_author and post.author_id != session['user_id']:
        abort(403)

    return post 


@views.route('/<int:id>/update', methods=('GET', 'POST'))
@login_required
def update(id):
    post = get_post(id)

    if request.method == 'POST':
        title = request.form['title']
        body = request.form['body']
        error = None

        if not title:
            error = 'Title is required.'

        if error is not None:
            flash(error)
        else:
            data = Post.query.get(post.id)
            data.title = title
            data.body = body
            db.session.commit()
        
            return redirect(url_for('views.index'))

    return render_template('update.html', post=post)

@views.route('/<int:id>/delete', methods=('POST',))
@login_required
def delete(id):
    post = get_post(id)
    data = Post.query.get(post.id)
    db.session.delete(data)
    db.session.commit()
    return redirect(url_for('views.index'))

