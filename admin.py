from flask import Blueprint, render_template, request, jsonify, abort, redirect, url_for
from slugify import slugify
from models import *
from flask_sqlalchemy import SQLAlchemy 

from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user

from flask_jwt_extended import (
    JWTManager, create_access_token, create_refresh_token,
    set_access_cookies, set_refresh_cookies,
     jwt_required,
    get_jwt_identity, unset_jwt_cookies
)

admin = Blueprint('admin', __name__, static_folder='static', template_folder='templates')

@admin.route('/')
@admin.route('/book')
@login_required
def book():
    new_user = Users.query.with_entities(Users.group_id).filter(Users.username == current_user.username).first()
    if new_user.group_id != 'admin':
        return redirect(url_for('index'))
    return render_template('admin/book.html')

@admin.route('/category')
@login_required
def category():
    new_user = Users.query.with_entities(Users.group_id).filter(Users.username == current_user.username).first()
    if new_user.group_id != 'admin':
        return redirect(url_for('index'))
    return render_template('admin/category.html')

@admin.route('/writer')
@login_required
def writer():
    new_user = Users.query.with_entities(Users.group_id).filter(Users.username == current_user.username).first()
    if new_user.group_id != 'admin':
        return redirect(url_for('index'))
    return render_template('admin/writer.html')

@admin.route('/group')
@login_required
def group():
    new_user = Users.query.with_entities(Users.group_id).filter(Users.username == current_user.username).first()
    if new_user.group_id != 'admin':
        return redirect(url_for('index'))
    return render_template('admin/group.html')

@admin.route('/user')
@login_required
def user():
    new_user = Users.query.with_entities(Users.group_id).filter(Users.username == current_user.username).first()
    if new_user.group_id != 'admin':
        return redirect(url_for('index'))
    return render_template('admin/user.html')