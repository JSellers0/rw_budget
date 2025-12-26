import os

from flask import Flask
from flask_sqlalchemy import SQLAlchemy

#from flask_bcrypt import Bcrypt
#from flask_login import LoginManager
from myfb import APP_SK, DB_H, DB_N, DB_P, DB_U, DB_Pt

app: Flask = Flask(__name__)

app.secret_key = APP_SK

db_uri = os.environ.get("")

app.config["SQLALCHEMY_ECHO"] = True
app.config["SQLALCHEMY_DATABASE_URI"] = db_uri
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db: SQLAlchemy = SQLAlchemy(app)
#bcrypt: Bcrypt = Bcrypt()
#bcrypt.init_app(app)

