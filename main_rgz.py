from werkzeug.security import check_password_hash, generate_password_hash
from flask import Blueprint, render_template, request, make_response, redirect, session, url_for
import psycopg2
from Db import db
from Db.models import users,articles
from flask_login import login_user, login_required, current_user, logout_user

main_rgz = Blueprint('main_rgz',__name__)

@main_rgz.route('/main_rgz')
def main_rgz():
    return "result in console!"