from flask import Blueprint, render_template, request, jsonify, abort, flash, json, url_for
from slugify import slugify
from datetime import datetime
from models import *
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

from itsdangerous import Serializer, TimedJSONWebSignatureSerializer, SignatureExpired

s = TimedJSONWebSignatureSerializer('Thisisasecret')

order = Blueprint('order', __name__, static_folder='static', template_folder='templates')

@order.route('/', methods=['POST'])
@jwt_required()
def index():
   sOrder = request.form['order']
   sMethod = request.form['payment-method']
   sCoupon = request.form['discount']

   for oOrder in json.loads(sOrder):
      new_book = Books.query.with_entities(Books.number, Books.title).\
         filter(Books.id == str(oOrder['id'])).first()
      if int(new_book.number) < int(oOrder['count']):
         return jsonify(
            message = new_book.title + ' is not enough!'
         ), 200

   sStatus = 'To pay'

   if sOrder == '' or sMethod == '':
      return jsonify(message = 'Invalid'), 200

   # datetime object containing current date and time
   now = datetime.now()
   # dd/mm/YY H:M:S
   dt_string = now.strftime("%d/%m/%Y %H:%M:%S")

   new_user = Users.query.\
      filter(Users.username == get_jwt_identity()).first()

   if sMethod == 'ibanking' or sMethod == 'cash':
      if sMethod == 'ibanking':
         token = s.dumps({
            'user_id' : new_user.id,
            'order' : sOrder,
            'method' : sMethod,
            'coupon' : sCoupon}).decode('utf-8')
         # datetime object containing current date and time
         now = datetime.now()
         # dd/mm/YY H:M:S
         dDateNow = now.strftime("%d/%m/%Y %H:%M:%S")
         if Tokens.query.filter(Tokens.user_id == new_user.id, Tokens.action == 'order').first():
            update_token = Tokens.query.filter(Tokens.user_id == new_user.id, Tokens.action == 'order').\
               update(dict(code = token, created = dDateNow, status  = 'created'))
         else:
            db_token = Tokens(new_user.id, 'order', token, dDateNow)
            db.session.add(db_token)
         db.session.commit()
         msg = Message('Confirm Order', sender = 'a06204995@gmail.com', recipients = [new_user.email])

         link = url_for('order.confirm_order', token=token, _external=True)

         msg.body = 'If you don’t use this link within 1 hours, it will expire. To confirm order, visit: {}'.format(link)
         mail.send(msg)
         return jsonify(
            message = 'Check your email for a link to confirm order. If it doesn’t appear within a few minutes, check your spam folder.'
         ), 200
      else:
         total = calculateTotal(sOrder, sCoupon)
         percent = ''
         if sCoupon != '':
            new_coupon = Coupons.query.with_entities(Coupons.percent).filter(Coupons.code == sCoupon).first()
            if new_coupon:
               percent = new_coupon.percent
         json_data = {
            'order' : sOrder,
            'coupon' : {'code': sCoupon, 'percent' : percent},
            'total' : round(total, 2)
         }
         new_order = Orders(new_user.id, json_data, sMethod, sStatus, dt_string, dt_string)
         db.session.add(new_order)

         db.session.commit()

         oOrder = Orders.query.with_entities(Orders.id).\
               filter(Orders.created == dt_string, Orders.user_id == new_user.id).first()

         msg = Message('Order success', sender = 'a06204995@gmail.com', recipients = [new_user.email])
         msg.body = 'Code: ' + str(oOrder.id) + \
                     '\nDate: ' + dt_string + \
                        '\nPayment method: ' + sMethod
         mail.send(msg)
               
         return jsonify(
            message = 'Order success'
         ), 200
   return jsonify(message="Invalid"), 200

@order.route('/confirm-order/<token>')
def confirm_order(token):
   try:
      id = s.loads(token)['user_id']
      sOrder = s.loads(token)['order']
      sMethod = s.loads(token)['method']
      sCoupon = s.loads(token)['coupon']

      sStatus = 'To pay'
      new_token = Tokens.query.filter(Tokens.user_id == id, Tokens.action == 'order').first()
      new_user = Users.query.filter(Users.id == id).first()
      if new_token:
         # check token
         if new_token.status == 'finish':   return render_template('client/message.html', message = 'The token is expired!')
         # datetime object containing current date and time
         now = datetime.now()
         # dd/mm/YY H:M:S
         dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
         dDateNow = datetime.strptime(dt_string, "%d/%m/%Y %H:%M:%S")

         dCreated = datetime.strptime(new_token.created, "%d/%m/%Y %H:%M:%S")
         time = dDateNow - dCreated
         if time.total_seconds() > 3600:
            return render_template('client/message.html', message = 'The token is expired!')
         
         # check money
         total = calculateTotal(sOrder, sCoupon)
         if total == 'error':
            return jsonify(
               message = 'error'
            ), 200

         if float(new_user.money) < float(total):
            return render_template('client/message.html', message = 'Your account does not have enough money!')
         
         new_money = float(new_user.money) - float(total)
         user_update = Users.query.\
            filter(Users.id == new_user.id).\
                  update(dict(money = str(new_money)))
         db.session.commit()
         # insert table order
         percent = ''
         if sCoupon != '':
            new_coupon = Coupons.query.with_entities(Coupons.percent).filter(Coupons.code == sCoupon).first()
            if new_coupon:
               percent = new_coupon.percent
         json_data = {
            'order' : sOrder,
            'coupon' : {'code': sCoupon, 'percent' : percent},
            'total' : round(total, 2)
         }
         new_order = Orders(new_user.id, json_data, sMethod, sStatus, dt_string, dt_string)
         db.session.add(new_order)

         db.session.commit()

         oOrder = Orders.query.with_entities(Orders.id).\
               filter(Orders.created == dt_string, Orders.user_id == new_user.id).first()

         msg = Message('Order success', sender = 'a06204995@gmail.com', recipients = [new_user.email])
         msg.body = 'Code: ' + str(oOrder.id) + \
                     '\nDate: ' + dt_string + \
                        '\nPayment method: ' + sMethod
         mail.send(msg)
         update_token = Tokens.query.filter(Tokens.user_id == id, Tokens.action == 'order').\
            update(dict(created = dDateNow, status = 'finish'))
         db.session.commit()
      else: return render_template('client/message.html', message = 'The token is expired!')
   except SignatureExpired:
      return render_template('client/message.html', message = 'The token is expired!')
   return render_template('client/message.html', message = 'Order success. Please check email!')

def calculateTotal(aData, sCoupon):
   aJsonId = json.loads(aData)
   total = 0
   for oData in aJsonId:
      if int(oData['id']) > 0 and int(oData['count']) > 0:
         new_book = Books.query.filter(Books.id == oData['id']).\
                  with_entities(Books.price).first()
         total = float(total) + float(new_book.price) * float(oData['count'])
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
               total = float(float(total) * float(new_coupon.percent))

   return round(total,2)

@order.route('/get-orders', methods=['POST'])
@jwt_required()
def get_orders():
   new_user = Users.query.with_entities(Users.id).filter(Users.username == get_jwt_identity()).first()

   new_order = Orders.query.filter(Orders.user_id == new_user.id).all()

   aOrder = []
   for oOrder in new_order:
      aOrder.append({
         'id' : oOrder.id,
         'created' : oOrder.created,
         'status' : oOrder.status,
         'total_price' : oOrder.order_info['total']
      })
   return jsonify(
      data = aOrder
   ), 200

@order.route('/get-detail-order', methods=['POST'])
@jwt_required()
def get_detail_orders():
   iId = request.form['id']
   new_user = Users.query.with_entities(Users.id).filter(Users.username == get_jwt_identity()).first()
   new_order = Orders.query.filter(Orders.id == iId, Orders.user_id == new_user.id).first()

   return jsonify(
      id = new_order.id,
      created = new_order.created,
      status = new_order.status,
      order_info = new_order.order_info,
      method = new_order.payment_info
   ), 200

@order.route('/cancel-order', methods=['POST'])
@jwt_required()
def cancel_order():
   iId = request.form['id']
   new_user = Users.query.with_entities(Users.id, Users.email).filter(Users.username == get_jwt_identity()).first()

   new_order = Orders.query.filter(Orders.id == iId, Orders.user_id == new_user.id).first()

   if new_order.status == 'To pay':
      upload_order = Orders.query.filter(Orders.id == iId).update(dict(status='Canceled'))
      db.session.commit()
      message = 'Canceled successfully!'

      msg = Message('Canceled successfully!', sender = 'a06204995@gmail.com', recipients = [new_user.email])
      msg.body = 'Canceled successfully!'
      mail.send(msg)
   else:    message = 'You can\'t delete it!'
   return jsonify(
      message = message
   ),200

@order.route('/get-all-order', methods=['POST'])
@jwt_required()
def get_all_orders():
   new_user = Users.query.with_entities(Users.group_id).filter(Users.username == get_jwt_identity()).first()
   if new_user.group_id == 'admin' or new_user.group_id == 'seller':
      page_num = request.form['page_num']
      if page_num == '':
         abort(404)

      new_order = Orders.query.order_by(Orders.id.asc()).\
         paginate(per_page=10, page=int(page_num), error_out=True)

      aOrder = []
      for oOrder in new_order.items:
         new_user = Users.query.\
            with_entities(Users.firstname, Users.lastname, Users.email, Users.address, Users.phone_number).\
               filter(Users.id == oOrder.user_id).first()
         aOrder.append({
            'id' : oOrder.id,
            'created' : oOrder.created,
            'status' : oOrder.status,
            'total_price' : oOrder.order_info['total'],
            'firstname' : new_user.firstname,
            'lastname' : new_user.lastname,
            'email' : new_user.email,
            'address' : new_user.address,
            'phone_number' : new_user.phone_number
         })
      return jsonify(
         items = aOrder,
         pages = new_order.pages,
         current_page = new_order.page,
         prev_num = new_order.prev_num,
         next_num = new_order.next_num
      ), 200
   return jsonify(
        message = 'You do not have permission to access!'
    ), 200
   
@order.route('/delete', methods=['DELETE'])
@jwt_required()
def delete():
   new_user = Users.query.with_entities(Users.group_id).filter(Users.username == get_jwt_identity()).first()
   if new_user.group_id == 'admin' or new_user.group_id == 'seller':
      id = request.form['id']
      oOrder = Orders.query.filter(Orders.id == id).first()
      db.session.delete(oOrder)
      db.session.commit()
      return jsonify(
         message = 'Deleted successfully!'
      ), 200
   return jsonify(
        message = 'You do not have permission to access!'
    ), 200

@order.route('/admin/get-detail-order', methods=['POST'])
@jwt_required()
def get_admin_detail_orders():
   new_user = Users.query.with_entities(Users.group_id).filter(Users.username == get_jwt_identity()).first()
   if new_user.group_id == 'admin' or new_user.group_id == 'seller':
      iId = request.form['id']
      new_order = Orders.query.filter(Orders.id == iId).first()

      return jsonify(
         id = new_order.id,
         created = new_order.created,
         status = new_order.status,
         order_info = new_order.order_info,
         method = new_order.payment_info
      ), 200
   return jsonify(
      message = 'You do not have permission to access!'
   ), 200

@order.route('/set-status', methods=['POST'])
@jwt_required()
def set_status():
   new_user = Users.query.with_entities(Users.group_id).filter(Users.username == get_jwt_identity()).first()
   if new_user.group_id == 'admin' or new_user.group_id == 'seller':
      iId = request.form['id']
      sStatus = request.form['status']
      upload_order = Orders.query.filter(Orders.id == iId).update(dict(status=sStatus))
      db.session.commit()

      if sStatus == 'To ship':
         new_order = Orders.query.with_entities(Orders.order_info).filter(Orders.id == iId).first()
         
         for oOrder in json.loads(new_order.order_info['order']):
            new_book = Books.query.with_entities(Books.number).filter(Books.id == str(oOrder['id'])).first()

            new_number = int(new_book.number) - int(oOrder['count'])
            upload_book = Books.query.filter(Books.id == str(oOrder['id'])).update(dict(number=str(new_number)))
            db.session.commit()

      return jsonify(
         message = 'Changed successfully!'
      ), 200
   return jsonify(
      message = 'You do not have permission to access!'
   ), 200
