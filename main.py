from werkzeug.security import check_password_hash, generate_password_hash
from flask import Blueprint, render_template, request, make_response, redirect, session
import psycopg2
from Db import db
from Db.models import users,articles
from flask_login import login_user, login_required, current_user, logout_user

main = Blueprint('main',__name__)

app.secret_key='321'
user_db = "ersh_RGZ"
host_ip = "127.0.0.1"
host_port = "5432"
database_name = "ersh_RGZ"
password = "123"

app.config['SQLALCHEMY_DATABASE_URI'] = f'postgresql://{user_db}:{password}@{host_ip}:{host_port}/{database_name}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

#Подключение Flask-Login
login_manager=LoginManager()
#Направление пользователя, если нет авторизации
login_manager.login_view = 'main.login'
login_manager.init_app(app)
#Где и как находить пользователя
@login_manager.user_loader
def load_users(user_id):
    return users.query.get(int(user_id))