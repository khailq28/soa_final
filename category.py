from flask import Blueprint, render_template, request, jsonify, abort, flash
from slugify import slugify
from datetime import datetime
from models import *
from flask_sqlalchemy import SQLAlchemy
from flask_login import current_user
from init import db

from flask_jwt_extended import (
    JWTManager, create_access_token, create_refresh_token,
    set_access_cookies, set_refresh_cookies,
     jwt_required,
    get_jwt_identity, unset_jwt_cookies
)

category = Blueprint('category', __name__, static_folder='static', template_folder='templates')

@category.route('/<string:slug>')
def index(slug):
   aCategory = Categories.query.with_entities(Categories.name).filter(Categories.slug == slug).first()
   return render_template('client/category.html', slug=slug, name=aCategory.name, user=current_user)

@category.route('/get-all-categories', methods=['POST'])
def getAllCategory():
   aCategory = Categories.query.all()
   aJsonCategory = []
   for oCategory in aCategory:
      aJsonCategory.append({
         'name' : oCategory.name,
         'slug' : oCategory.slug,
         'created' : oCategory.created
      })
   return jsonify(
      category= aJsonCategory
   ), 200

@category.route('/add-category', methods=['POST'])
@jwt_required()
def addCategory():
   if request.method == 'POST':
      new_user = Users.query.with_entities(Users.group_id).filter(Users.username == get_jwt_identity()).first()
      if new_user.group_id != 'admin':
         return jsonify(
            message = 'You do not have permission to access!'
         ), 200
      sName = request.form['name']
      sSlug = slugify(sName)

      # datetime object containing current date and time
      now = datetime.now()
      # dd/mm/YY H:M:S
      dDateNow = now.strftime("%d/%m/%Y %H:%M:%S")
      #create new category
      oCategory = Categories(sName, sSlug, dDateNow, dDateNow)

      #insert into table
      db.session.add(oCategory)
      db.session.commit()

      return jsonify(
         message = 'Category added successfully!'
      ), 200

@category.route('/delete', methods=['DELETE'])
@jwt_required()
def delete():
   new_user = Users.query.with_entities(Users.group_id).filter(Users.username == get_jwt_identity()).first()
   if new_user.group_id != 'admin':
      return jsonify(
         message = 'You do not have permission to access!'
      ), 200
   name = request.form['name']
   oCategory = Categories.query.filter(Categories.name == name).first()
   db.session.delete(oCategory)
   db.session.commit()
   return jsonify(
      message = 'Deleted successfully!'
   ), 200

