from werkzeug.security import check_password_hash, generate_password_hash
from flask import Flask, Blueprint, render_template, request, make_response, redirect, url_for
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
            # Проверка наличия анкеты у пользователя
            user_form = form.query.filter_by(user_id=my_user.id).first()
            if user_form is None:
                return redirect('/page')
            else:
                return redirect('/main')
    return redirect('/login')



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



@app.route('/main', methods=['POST', 'GET'])
def main():
    errors = ''
    findname_form=request.form.get('findname')
    findage_form=request.form.get('findage')
    return render_template('main.html',username=current_user.username)


#Выход из аккаунта
@app.route('/main/logout')
@login_required
def logout():
    logout_user()
    return redirect('/login')


#Удаление аккаунта
@app.route('/main/delete', methods=['POST'])
@login_required
def delete():
    user_id = current_user.id
    user = users.query.get(user_id)
    db.session.delete(user)
    db.session.commit()
    logout_user()
    return redirect('/login')

#Страница анкеты
@app.route('/page', methods=['POST', 'GET'])
@login_required
def page():
    if request.method=='GET':
        return render_template('page.html')

    name = request.form.get('urname')
    gender = request.form.get('urmale')
    search_gender = request.form.get('urfindmale')
    about = request.form.get('urinfo')
    photo = request.form.get('urphoto')
    user_id = current_user.id

    if request.form.get('urage') == '':
        age=request.form.get('urage')
    else:
        age = int(request.form.get('urage'))
        if age<18 or age>100:
            errors='Некорректный возраст'
            return render_template('page.html',errors=errors,urname=name,urmale=gender,urfindmale=search_gender,urinfo=about,urphoto=photo)
    
    if name=='' or gender=='' or search_gender=='':
        errors='Пожалуйста, заполните все поля'
        return render_template('page.html',errors=errors,urname=name,urage=age,urmale=gender,urfindmale=search_gender,urinfo=about,urphoto=photo)
    

    new_form = form(user_id=user_id, name=name, age=age, gender=gender, search_gender=search_gender, about=about, photo=photo)
    db.session.add(new_form)
    db.session.commit()
    return redirect('/main')

#Редактирование анкеты
@app.route('/main/page_change', methods=['POST', 'GET'])
@login_required
def page_change():
    user_id = current_user.id
    existing_form = form.query.filter_by(user_id=user_id).first()
    
    if request.method == 'GET':
        return render_template('page_change.html', form=existing_form)

    name = request.form.get('urname')
    gender = request.form.get('urmale')
    search_gender = request.form.get('urfindmale')
    about = request.form.get('urinfo')
    photo = request.form.get('urphoto')
    
    if request.form.get('urage') == '':
        age = None
    else:
        age = int(request.form.get('urage'))
        if age < 18 or age > 100:
            errors = 'Некорректный возраст'
            return render_template('page_change.html', errors=errors, form=existing_form)
    
    if name == '' or gender == '' or search_gender == '':
        errors = 'Пожалуйста, заполните все поля'
        return render_template('page_change.html', errors=errors, form=existing_form)

    existing_form.name = name
    existing_form.age = age
    existing_form.gender = gender
    existing_form.search_gender = search_gender
    existing_form.about = about
    existing_form.photo = photo

    db.session.commit()
    return redirect('/main')

#Скрыть анкету


