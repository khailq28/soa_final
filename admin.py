from flask import Blueprint, render_template, request, jsonify, abort
from slugify import slugify
from models import *
from flask_sqlalchemy import SQLAlchemy 

admin = Blueprint('admin', __name__, static_folder='static', template_folder='templates')

#function

