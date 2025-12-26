import os

from flask import Flask
from flask_sqlalchemy import SQLAlchemy

#from flask_bcrypt import Bcrypt
#from flask_login import LoginManager

from logging_config import setup_logging

app: Flask = Flask(__name__)

app.secret_key = os.environ.get("FLASK_SECRET_KEY")

db_uri = os.environ.get("FLASK_DATABASE_URL")

app.config["SQLALCHEMY_ECHO"] = True
app.config["SQLALCHEMY_DATABASE_URI"] = db_uri
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db: SQLAlchemy = SQLAlchemy(app)

setup_logging(app)
    
app.logger.info('Application started')
#bcrypt: Bcrypt = Bcrypt()
#bcrypt.init_app(app)

