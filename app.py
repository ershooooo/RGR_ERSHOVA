from flask import Flask, session
from flask_sqlalchemy import SQLAlchemy
from Db import db
from Db.models import users
from flask_login import LoginManager
from main_rgz import main_rgz

app = Flask(__name__)

app.secret_key='123'
user_db = "ershova"
host_ip = "127.0.0.1"
host_port = "5432"
database_name = "ershova_RGZ"
password = "123"

app.config['SQLALCHEMY_DATABASE_URI'] = f'postgresql://{user_db}:{password}@{host_ip}:{host_port}/{database_name}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

#Подключение Flask-Login
login_manager=LoginManager()
#Направление пользователя, если нет авторизации
login_manager.login_view = 'lab6.login'
login_manager.init_app(app)
#Где и как находить пользователя
@login_manager.user_loader
def load_users(user_id):
    return users.query.get(int(user_id))

