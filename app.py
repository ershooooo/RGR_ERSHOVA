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
database_name = "ershova_rgz"
password = "123"


app.config['SQLALCHEMY_DATABASE_URI'] = f'postgresql://{user_db}:{password}@{host_ip}:{host_port}/{database_name}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False 
db.init_app(app)


login_manager=LoginManager()
login_manager.login_view = 'app.login'
login_manager.init_app(app)
@login_manager.user_loader
def load_users(user_id):
    return users.query.get(int(user_id))



@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method=='GET':
        return render_template('login.html')
    
    errors=''
    username_form=request.form.get('username')
    password_form=request.form.get('password')

    #Ошибка: поля не заполнены
    if username_form =='' or password_form == '':
        errors='Пожалуйста, заполните все поля'
        return render_template('login.html',errors=errors,username=username_form,password=password_form)

    my_user=users.query.filter_by(username=username_form).first()
    
    #Ошибка: пользователь отсутствует    
    if my_user is None:
        errors='Такой пользователь отсутствует'
        return render_template('login.html',errors=errors,username=username_form,password=password_form)
    #Ошибка неправильного пороля
    if not check_password_hash(my_user.password, password_form):
        errors = 'Введен неправильный пароль'
        return render_template('login.html', errors=errors,username=username_form)

    if my_user is not None:
        if check_password_hash(my_user.password, password_form):
            #Сохраняем JWT токен
            login_user(my_user,remember=False)
            return redirect('/login')
    return render_template('login.html',username=current_user.username)



@app.route('/register', methods=['POST', 'GET'])
def register():
    if request.method=='GET':
        return render_template('register.html')

    errors = ''
    username_form=request.form.get('username')
    password_form=request.form.get('password')
    password_2_form=request.form.get('password_2')

    #Ошибка: поля не заполнены
    if username_form =='' or password_form == '' or password_2_form == '':
        errors='Пожалуйста, заполните все поля'
        return render_template('register.html',errors=errors,username=username_form,password=password_form,password_2=password_2_form)

    #Проверка, что такой пользователь отсуствует 
    isUserExist = users.query.filter_by(username=username_form).first()
    if isUserExist is not None:
        errors='Пользователь с данным именем уже существует'
        return render_template('register.html',errors=errors,password=password_form,password_2=password_2_form)

    #Проверка, что пароль и подтверждение пароля совпадают
    if password_form == password_2_form:
        pass
    else:
        errors = 'Подтверждение пароля не совпадает'
        return render_template('register.html',errors=errors,username=username_form)

    #Проверка, что пароль больше 5 символов
    if len(password_form) < 5:
        errors='Придумайте более сложный пароль'
        return render_template('register.html',errors=errors,username=username_form)

   #Хэшируем пароль
    hashedPswd = generate_password_hash(password_form, method='pbkdf2')
   #Создаем объект users с нужными полями 
    newUser = users(username=username_form,password=hashedPswd)
    db.session.add(newUser)
    db.session.commit()
    return redirect('/login')