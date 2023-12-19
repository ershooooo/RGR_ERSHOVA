#Импортируем переменную db из файла __init.py__
from . import db
from flask_login import UserMixin
from sqlalchemy.orm import relationship
from datetime import datetime

#Описываем схему нашей БД в виде объектов таким образом, создание таблиц (схемы БД)
#Возьмет на себя SQLAlchemy - система ORM.abs

class users(db.Model,UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(30), nullable=False, unique=True)
    password = db.Column(db.String(1024), nullable=False)
    

    def __repr__(self):
        return f'id:{self.id}, username:{self.username}'
        

class articles(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    title = db.Column(db.String(50), nullable=False)
    article_text = db.Column(db.Text, nullable=False)
    is_favorite = db.Column(db.Boolean, default=False)
    is_public = db.Column(db.Boolean, default=False)
    likes = db.Column(db.Integer,default=0)
    

    def __repr__(self):
        return f'id:{self.id},title:{self.title}, article_text:{self.article_text}'

class Form(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    age = db.Column(db.Integer, nullable=False)
    gender = db.Column(db.String(10), nullable=False)
    search_gender = db.Column(db.String(10), nullable=False)
    about = db.Column(db.String(200))
    photo = db.Column(db.String(100))

    def __repr__(self):
        return f"Form('{self.name}', '{self.age}', '{self.gender}', '{self.search_gender}')"