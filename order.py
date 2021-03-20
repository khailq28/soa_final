from flask import Blueprint, render_template, request, jsonify, abort, flash
from slugify import slugify
from datetime import datetime
from models import Orders
from flask_sqlalchemy import SQLAlchemy
from init import db

order = Blueprint('order', __name__, static_folder='static', template_folder='templates')

@order.route('/')
def index():
   return 'sds'
