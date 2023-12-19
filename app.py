from werkzeug.security import check_password_hash, generate_password_hash
from flask import Flask, Blueprint, render_template, request, make_response, redirect
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from Db import db
from Db.models import users, form
from flask_login import UserMixin
from flask_login import login_user, login_required, current_user, logout_user


app = Flask(__name__)


app.secret_key = '123'
user_db = "ershova"
host_ip = "localhost"
host_port = "5432"
database_name = "ershova_RGZ"
password = "123"


app.config['SQLALCHEMY_DATABASE_URI'] = f'postgresql://{user_db}:{password}@{host_ip}:{host_port}/{database_name}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False 
db.init_app(app)


#Подключение Flask-Login
login_manager=LoginManager()
#Направление пользователя, если нет авторизации
login_manager.login_view = 'app.login'
login_manager.init_app(app)
@login_manager.user_loader
def load_users(user_id):
    return users.query.get(int(user_id))