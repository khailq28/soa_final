from flask import Blueprint, render_template, request, jsonify, abort, flash
from slugify import slugify
from datetime import datetime
from models import Groups
from flask_sqlalchemy import SQLAlchemy
from init import db

group = Blueprint('group', __name__, static_folder='static', template_folder='templates')

