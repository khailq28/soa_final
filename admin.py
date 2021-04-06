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
    if new_user.group_id == 'admin' or new_user.group_id == 'seller':
        admin = True
        if new_user.group_id == 'seller':   admin = False
        return render_template('admin/book.html', admin = admin)
    return redirect(url_for('index'))

@admin.route('/category')
@login_required
def category():
    new_user = Users.query.with_entities(Users.group_id).filter(Users.username == current_user.username).first()
    if new_user.group_id != 'admin':
        return redirect(url_for('index'))
    return render_template('admin/category.html', admin = True)

@admin.route('/writer')
@login_required
def writer():
    new_user = Users.query.with_entities(Users.group_id).filter(Users.username == current_user.username).first()
    if new_user.group_id != 'admin':
        return redirect(url_for('index'))
    return render_template('admin/writer.html', admin = True)

@admin.route('/group')
@login_required
def group():
    new_user = Users.query.with_entities(Users.group_id).filter(Users.username == current_user.username).first()
    if new_user.group_id != 'admin':
        return redirect(url_for('index'))
    return render_template('admin/group.html', admin = True)

@admin.route('/user')
@login_required
def user():
    new_user = Users.query.with_entities(Users.group_id).filter(Users.username == current_user.username).first()
    if new_user.group_id != 'admin':
        return redirect(url_for('index'))
    return render_template('admin/user.html', admin = True)

@admin.route('/order')
@login_required
def order():
    new_user = Users.query.with_entities(Users.group_id).filter(Users.username == current_user.username).first()
    if new_user.group_id == 'admin' or new_user.group_id == 'seller':
        admin = True
        if new_user.group_id == 'seller':   admin = False
        return render_template('admin/order.html', admin = admin)
    return redirect(url_for('index'))

@admin.route('/detail/<id>')
@login_required
def detail(id):
    new_user = Users.query.with_entities(Users.group_id).filter(Users.username == current_user.username).first()
    if new_user.group_id == 'admin' or new_user.group_id == 'seller':
        return render_template('client/order-detail.html', id = id, admin=True)
    return redirect(url_for('index'))
    

@admin.route('/get-user-info', methods=['POST'])
@jwt_required()
def get_info():
    new_user = Users.query.with_entities(Users.group_id).filter(Users.username == get_jwt_identity()).first()
    if new_user.group_id == 'admin' or new_user.group_id == 'seller':
        id = request.form['id']
        new_order = Orders.query.with_entities(Orders.user_id).filter(Orders.id == id).first()
        new_user = Users.query.\
            with_entities(Users.firstname, Users.lastname, Users.username, Users.address, Users.phone_number, Users.money, Users.email).\
                filter(Users.id == new_order.user_id).first()
        return jsonify(
            firstname = new_user.firstname,
            lastname = new_user.lastname,
            username = new_user.username,
            address = new_user.address,
            phone = new_user.phone_number,
            money = new_user.money,
            email = new_user.email
        ), 200
    return jsonify(
        message = 'You do not have permission to access!'
    ), 200