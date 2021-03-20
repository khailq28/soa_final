from flask import Blueprint, render_template, request, jsonify, abort, flash
from slugify import slugify
from datetime import datetime
from models import Coupons
from flask_sqlalchemy import SQLAlchemy
from init import db

coupon = Blueprint('coupon', __name__, static_folder='static', template_folder='templates')
