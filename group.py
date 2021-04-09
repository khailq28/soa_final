from flask import Blueprint, render_template, request, jsonify, abort, flash
from slugify import slugify
from datetime import datetime
from models import *
from flask_sqlalchemy import SQLAlchemy
from init import db

from flask_jwt_extended import (
    JWTManager, create_access_token, create_refresh_token,
    set_access_cookies, set_refresh_cookies,
     jwt_required,
    get_jwt_identity, unset_jwt_cookies
)

group = Blueprint('group', __name__, static_folder='static', template_folder='templates')

@group.route('/get-all-group', methods=['POST'])
@jwt_required()
def getDataGroup():
    new_user = Users.query.with_entities(Users.group_id).filter(Users.username == get_jwt_identity()).first()
    if new_user.group_id != 'admin':
        return jsonify(
            message = 'You do not have permission to access!'
        ), 200

    aGroup = Groups.query.order_by(Groups.name.asc()).all()
    aJsonGroup = []
    for oGroup in aGroup:
        aJsonGroup.append({
            'name' : oGroup.name,
            'description' : oGroup.description,
            'created' : oGroup.created
        })
    return jsonify(
        items = aJsonGroup
    )

@group.route('/add-group', methods=['POST'])
@jwt_required()
def addGroup():
    new_user = Users.query.with_entities(Users.group_id).filter(Users.username == get_jwt_identity()).first()
    if new_user.group_id != 'admin':
        return jsonify(
            message = 'You do not have permission to access!'
        ), 200
    
    sName = request.form['name']
    sDescription = request.form['description']
    sSlug = slugify(sName)

    # datetime object containing current date and time
    now = datetime.now()
    # dd/mm/YY H:M:S
    dDateNow = now.strftime("%d/%m/%Y %H:%M:%S")
    #create new writer
    oGroup = Groups(sName, sDescription, dDateNow)

    #insert into table
    db.session.add(oGroup)
    db.session.commit()
    return jsonify( 
        message = 'Group added successfully!'
    ), 200

@group.route('/delete', methods=['DELETE'])
@jwt_required()
def delete():
    new_user = Users.query.with_entities(Users.group_id).filter(Users.username == get_jwt_identity()).first()
    if new_user.group_id != 'admin':
        return jsonify(
            message = 'You do not have permission to access!'
        ), 200

    name = request.form['name']
    oGroup = Groups.query.filter(Groups.name == name).first()
    db.session.delete(oGroup)
    db.session.commit()
    return jsonify( 
        message = 'Deleted successfully!'
    ), 200
