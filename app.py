from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from myfb import APP_SK, DB_U, DB_P, DB_H
import os

app: Flask = Flask(__name__)

app.secret_key = APP_SK

# ToDo: dev - sqlite

db_uri = f"mysql+pymysql://{DB_U}:{DB_P}@{DB_H}/rw_budget"

app.config["SQLALCHEMY_ECHO"] = True
app.config["SQLALCHEMY_DATABASE_URI"] = db_uri
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db: SQLAlchemy = SQLAlchemy(app)
bcrypt: Bcrypt = Bcrypt()
bcrypt.init_app(app)

