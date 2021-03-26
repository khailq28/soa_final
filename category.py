from flask import Blueprint, render_template, request, jsonify, abort, flash
from slugify import slugify
from datetime import datetime
from models import Categories
from flask_sqlalchemy import SQLAlchemy
from flask_login import current_user
from init import db

category = Blueprint('category', __name__, static_folder='static', template_folder='templates')

@category.route('/<string:slug>')
def index(slug):
   aCategory = Categories.query.with_entities(Categories.name).filter(Categories.slug == slug).first()
   return render_template('client/category.html', slug=slug, name=aCategory.name, user=current_user)

@category.route('/get-all-categories', methods=['POST'])
def getAllCategory():
   aCategory = Categories.query.with_entities(Categories.name, Categories.slug).all()
   aJsonCategory = []
   for oCategory in aCategory:
      aJsonCategory.append({
         'name' : oCategory.name,
         'slug' : oCategory.slug
      })
   return jsonify(
      category= aJsonCategory
   ), 200

