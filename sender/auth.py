import functools
import json

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.security import check_password_hash, generate_password_hash

from . import mongo

bp = Blueprint('auth', __name__, url_prefix='/auth')


def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('auth.login'))
        return view(**kwargs)

    return wrapped_view


@bp.route('/register', methods=('GET', 'POST'))
def register():
    if request.method == 'POST':
        data = json.loads(request.data.decode('utf-8'))
        email = data.get('email')
        password = data.get('password')
        error = None

        if not email:
            error = 'Email is required.'
        elif not password:
            error = 'Password is required.'
        elif mongo.db.users.find_one({'email': email}):
            error = 'Email {} is already registered.'.format(email)

        if error:
            return {'error': error}
        else:
            mongo.db.users.insert_one({'email': email, 'password': generate_password_hash(password)})
            return {'error': None}

    return render_template('auth/register.html')


@bp.route('/login', methods=('GET', 'POST'))
def login():
    if request.method == 'POST':
        data = json.loads(request.data.decode('utf-8'))
        email = data.get('email')
        password = data.get('password')
        error = None
        user = mongo.db.users.find_one({'email': email})

        if user is None:
            error = 'Incorrect email.'
        elif not check_password_hash(user['password'], password):
            error = 'Incorrect password.'

        if error:
            return {'error': error}
        else:
            session.clear()
            session['email'] = user['email']
            return {'error': None}

    return render_template('auth/login.html')


@bp.before_app_request
def load_logged_in_user():
    email = session.get('email')

    if email is None:
        g.user = None
    else:
        g.user = mongo.db.users.find_one({'email': email})


@bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))
