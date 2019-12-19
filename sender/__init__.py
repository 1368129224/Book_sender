import os
from flask import Flask


UPLOAD_FOLDER = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'books')
app = Flask(__name__, instance_relative_config=True)
app.config.from_mapping(
    SECRET_KEY='dev',
    UPLOAD_FOLDER=UPLOAD_FOLDER,
    MAX_CONTENT_LENGTH=25 * 1024 * 1024,
)

from . import sender
app.register_blueprint(sender.bp)
app.add_url_rule('/', endpoint='index')
