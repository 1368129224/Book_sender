import os
from flask import Flask
from flask_pymongo import PyMongo


UPLOAD_FOLDER = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'books')
app = Flask(__name__, instance_relative_config=True)
app.config.from_mapping(
    SECRET_KEY='dev',
    UPLOAD_FOLDER=UPLOAD_FOLDER,
    MAX_CONTENT_LENGTH=25 * 1024 * 1024,
    MONGO_URI='mongodb://192.168.194.129:27017/book_sender',
)
mongo = PyMongo(app)

from . import auth, sender
app.register_blueprint(auth.bp)
app.register_blueprint(sender.bp)
app.add_url_rule('/', endpoint='index')

