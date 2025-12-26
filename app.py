import os
from dotenv import load_dotenv
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from logging_config import setup_logging

load_dotenv()

app: Flask = Flask(__name__)

app.secret_key = os.environ.get("SECRET_KEY")
db_uri = os.environ.get("DATABASE_URL")

app.config["SQLALCHEMY_ECHO"] = True
app.config["SQLALCHEMY_DATABASE_URI"] = db_uri
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db: SQLAlchemy = SQLAlchemy(app)

if os.environ.get("FLASK_ENV", "development") == "production":
    setup_logging(app)
    
app.logger.info('Application started')

