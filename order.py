from flask import Blueprint, render_template, request, jsonify, abort, flash, json
from slugify import slugify
from datetime import datetime
from models import Orders, Users, Books, Coupons
from flask_mail import Message
from flask_sqlalchemy import SQLAlchemy
from init import db, mail
import random

from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user

from flask_jwt_extended import (
    JWTManager, create_access_token, create_refresh_token,
    set_access_cookies, set_refresh_cookies,
     jwt_required,
    get_jwt_identity, unset_jwt_cookies
)

order = Blueprint('order', __name__, static_folder='static', template_folder='templates')

@order.route('/get_otp', methods=['POST'])
@jwt_required()
def getOtp():
    otp = random.randrange(100000, 1000000)

    # datetime object containing current date and time
    now = datetime.now()
    # dd/mm/YY H:M:S
    dt_string = now.strftime("%d/%m/%Y %H:%M:%S")

    update_user = Users.query.filter(Users.username == get_jwt_identity()).\
        update(dict(otp=otp, created_otp=dt_string))
    db.session.commit()

    new_user = Users.query.with_entities(Users.email).filter(Users.username == get_jwt_identity()).first()

    msg = Message('Confirm payment', sender = 'a06204995@gmail.com', recipients = [new_user.email])
    msg.body = 'OTP (expires after 5 minutes): ' + str(otp)
    mail.send(msg)

    return 'OTP is sent to your email!', 200

@order.route('/', methods=['POST'])
@jwt_required()
def index():
   sOrder = request.form['order']
   sMethod = request.form['payment-method']
   sCoupon = request.form['discount']

   sStatus = 'To pay'

   if sOrder == '' or sMethod == '':
      return jsonify(message = 'Invalid'), 200

   # datetime object containing current date and time
   now = datetime.now()
   # dd/mm/YY H:M:S
   dt_string = now.strftime("%d/%m/%Y %H:%M:%S")

   if sMethod == 'ibanking' or sMethod == 'cash':
      if sMethod == 'ibanking':
         sOTP = request.form['OTP']
         new_user = Users.query.with_entities(Users.id, Users.otp, Users.created_otp, Users.money).\
            filter(Users.username == get_jwt_identity()).first()
         if new_user.otp == sOTP:
            created_otp = datetime.strptime(new_user.created_otp, "%d/%m/%Y %H:%M:%S")

            time_now = datetime.strptime(dt_string, "%d/%m/%Y %H:%M:%S")

            a = time_now - created_otp
            
            if a.total_seconds() >= 300:
               return jsonify(
                  message = 'OTP expired'
               ), 200
            
            if calculateTotal(sOrder, sCoupon) == 'error':
               return jsonify(
                  message = 'error'
               ), 200

            if int(new_user.money) < int(calculateTotal(sOrder, sCoupon)):
               return jsonify(
                  message = 'Your account does not have enough money!'
               ), 200
            
            new_money = int(new_user.money) - int(calculateTotal(sOrder, sCoupon))
            user_update = Users.query.\
               filter(Users.id == new_user.id).\
                     update(dict(money = str(new_money), otp = '', created_otp = ''))

            db.session.commit()
            sStatus = 'Check out'

      json_data = {
         'order' : sOrder,
         'coupon' : sCoupon
      }
      new_user = Users.query.with_entities(Users.id, Users.email).\
            filter(Users.username == get_jwt_identity()).first()
      new_order = Orders(new_user.id, json_data, sMethod, sStatus, dt_string, dt_string)
      db.session.add(new_order)

      db.session.commit()

      oOrder = Orders.query.with_entities(Orders.id).\
            filter(Orders.created == dt_string, Orders.user_id == new_user.id).first()

      msg = Message('Order success', sender = 'a06204995@gmail.com', recipients = [new_user.email])
      msg.body = 'Code: ' + str(oOrder.id) + \
                  '\nDate: ' + dt_string + \
                     'Payment method: ' + sMethod
      mail.send(msg)
            
      return jsonify(
         message = 'Order success'
      ), 200
   return jsonify(message="Invalid"), 200

def calculateTotal(aData, sCoupon):
   aJsonId = json.loads(aData)
   total = 0
   for oData in aJsonId:
      if int(oData['id']) > 0 and int(oData['count']) > 0:
         new_book = Books.query.filter(Books.id == oData['id']).\
                  with_entities(Books.price).first()
         total = int(total) + int(new_book.price) * int(oData['count'])
      else:
         return 'error'

   if sCoupon != '':
      new_coupon = Coupons.query.filter(Coupons.code == sCoupon).first()
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
               total = int(int(total) * float(new_coupon.percent))

   return total

   
   
