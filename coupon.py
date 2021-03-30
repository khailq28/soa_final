from flask import Blueprint, render_template, request, jsonify, abort, flash
from slugify import slugify
from datetime import datetime
from models import Coupons
from flask_sqlalchemy import SQLAlchemy
from init import db

coupon = Blueprint('coupon', __name__, static_folder='static', template_folder='templates')

@coupon.route('/check-coupon', methods=['POST'])
def check_coupon():
   sCode = request.form['code']

   if sCode == '':
      return jsonify(
         message = 'Code does not exist!'
      ), 200

   new_coupon = Coupons.query.filter(Coupons.code == sCode).first()
   if new_coupon:
      # datetime object containing current date and time
      now = datetime.now()
      # dd/mm/YY H:M:S
      dDateNow = now.strftime("%d/%m/%Y %H:%M:%S")

      dDateNow = datetime.strptime(dDateNow, "%d/%m/%Y %H:%M:%S")

      dStart = datetime.strptime(new_coupon.time_start, "%d/%m/%Y %H:%M:%S")
      dEnd = datetime.strptime(new_coupon.time_end, "%d/%m/%Y %H:%M:%S")

      a = dDateNow - dStart
      b = dDateNow - dEnd

      if a.total_seconds() > 0 and b.total_seconds() < 0:
         return  jsonify(
            percent = new_coupon.percent,
         ), 200
      else:
         return  jsonify(
            message = 'Code has expired!'
         ), 200
   return jsonify(
      message = 'Code does not exist!'
   ), 200
