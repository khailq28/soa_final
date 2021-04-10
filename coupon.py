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

@coupon.route('/get-all-coupon', methods=['POST'])
@jwt_required()
def getAllCoupon():
   new_user = Users.query.with_entities(Users.group_id).filter(Users.username == get_jwt_identity()).first()
   if new_user.group_id != 'admin':
      return jsonify(
         message = 'You do not have permission to access!'
      ), 200

   aCoupon = Coupons.query.all()
   aJsonCoupon = []
   for aCoupon in aCoupon:
      aJsonCoupon.append({
         'code' : aCoupon.code,
         'percent' : aCoupon.percent,
         'description' : aCoupon.description,
         'time_start' : aCoupon.time_start,
         'time_end' : aCoupon.time_end,
         'created' : aCoupon.created
      })
   return jsonify(
      items = aJsonCoupon
   )

@coupon.route('/add-coupon', methods=['POST'])
@jwt_required()
def addCoupon():
   new_user = Users.query.with_entities(Users.group_id).filter(Users.username == get_jwt_identity()).first()
   if new_user.group_id != 'admin':
      return jsonify(
         message = 'You do not have permission to access!'
      ), 200
   
   sCode = request.form['code']
   sPercent = float(int(request.form['percent']) / 100)
   sDescription = request.form['description']

   aTimeStart = []
   for oTimeStart in request.form['time-start'].split('-'):
      aTimeStart.append(oTimeStart)
   
   sTimeStart = aTimeStart[2] + '/' + aTimeStart[1] + '/' + aTimeStart[0] + ' 00:00:01'

   aTimeEnd = []
   for oTimeEnd in request.form['time-end'].split('-'):
      aTimeEnd.append(oTimeEnd)
   
   sTimeEnd = aTimeEnd[2] + '/' + aTimeEnd[1] + '/' + aTimeEnd[0] + ' 00:00:01'

   # datetime object containing current date and time
   now = datetime.now()
   # dd/mm/YY H:M:S
   dDateNow = now.strftime("%d/%m/%Y %H:%M:%S")
   #create new writer
   oCoupon = Coupons(sCode, sPercent, sDescription, sTimeStart, sTimeEnd, dDateNow)

   #insert into table
   db.session.add(oCoupon)
   db.session.commit()
   return jsonify( 
      message = 'Coupon added successfully!'
   ), 200


@coupon.route('/delete', methods=['DELETE'])
@jwt_required()
def delete():
    new_user = Users.query.with_entities(Users.group_id).filter(Users.username == get_jwt_identity()).first()
    if new_user.group_id != 'admin':
        return jsonify(
            message = 'You do not have permission to access!'
        ), 200

    code = request.form['code']
    oCoupon = Coupons.query.filter(Coupons.code == code).first()
    db.session.delete(oCoupon)
    db.session.commit()
    return jsonify( 
        message = 'Deleted successfully!'
    ), 200