import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_mail import Mail

from dotenv import find_dotenv, load_dotenv
load_dotenv(find_dotenv())

app = Flask(__name__)
FLASK_ENV = 'production'
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('SQLALCHEMY_DATABASE_URI')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message_category = 'info'
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
app.config['MAIL_USERNAME'] = os.environ.get('EMAIL_USERNAME')
app.config['MAIL_PASSWORD'] = os.environ.get('EMAIL_PASSWORD')
mail = Mail(app)

userStrings = []
with open("user-agents.txt") as f:
    userStrings = f.readlines()

from package import route
