from flask import Flask, render_template, request, jsonify, url_for, redirect
from models import *
from admin import admin
from category import category
from book import book
from coupon import coupon
from group import group
from order import order
from writer import writer
from init import app, db, mail
from datetime import datetime
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash

from flask_jwt_extended import (
    JWTManager, create_access_token, create_refresh_token,
    set_access_cookies, set_refresh_cookies,
     jwt_required,
    get_jwt_identity, unset_jwt_cookies
)

from flask_mail import Message
from itsdangerous import Serializer, TimedJSONWebSignatureSerializer, SignatureExpired

s = TimedJSONWebSignatureSerializer('Thisisasecret')

app.register_blueprint(admin, url_prefix='/admin')
app.register_blueprint(book, url_prefix='/book')
app.register_blueprint(category, url_prefix='/category')
app.register_blueprint(coupon, url_prefix='/coupon')
app.register_blueprint(group, url_prefix='/group')
app.register_blueprint(order, url_prefix='/order')
app.register_blueprint(writer, url_prefix='/writer')

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'signin'

@login_manager.user_loader
def load_user(user_id):
    return Users.query.get(int(user_id))

@app.route('/')
@app.route('/home')
def index():
   return render_template('client/home.html', user=current_user)

@app.route('/my-cart')
def my_cart():
   return render_template('client/cart.html')

@app.route('/detail/<id>')
@login_required
def order_detail(id):
   return render_template('client/order-detail.html', id = id)

@app.route('/my-info')
@login_required
def my_info():
   return render_template('client/my-info.html', user=current_user)

@app.route('/my-orders')
@login_required
def my_orders():
   return render_template('client/list-order.html', user=current_user)

@app.route('/signin', methods=['GET', 'POST'])
def signin():
   if request.method == 'POST':
      sUsername = request.form['i-username']
      sPassword = request.form['i-password']
      user = Users.query.filter(Users.username == sUsername).first()
      if user:
         if check_password_hash(user.password, sPassword):
               login_user(user)
               access_token = create_access_token(identity=sUsername, fresh=True)
               resp = jsonify({
                  'login': True,
                  'token': access_token
               })
               return resp, 200

      return jsonify(
         login = False,
         message = 'Invalid username or password'
      ), 200

   if current_user.is_authenticated:
      return redirect(url_for('index'))
   return render_template('client/signin.html')

@app.route('/signup', methods=['POST'])
def signup():
   sLastname = request.form['lastname']
   sFirstname = request.form['firstname']
   sUsername = request.form['username']
   sPassword = request.form['password']
   sConfirm = request.form['confirm']
   sEmail = request.form['email']
   sAddress = request.form['address']
   sPhone = request.form['phone']
   if sPassword != sConfirm:
      return jsonify(
         message = "Invalid"
      ), 200

   if sLastname != '' and sFirstname != '' and sUsername != '' and sPassword != '' and sEmail != '' and sAddress != '' and sPhone != '':
      hashed_password = generate_password_hash(sPassword, method='sha256')
      
      # datetime object containing current date and time
      now = datetime.now()
      # dd/mm/YY H:M:S
      dDateNow = now.strftime("%d/%m/%Y %H:%M:%S")

      oUser = Users(sUsername, hashed_password, sEmail, sFirstname, sLastname, sAddress, sPhone, dDateNow, dDateNow)
      db.session.add(oUser)
      db.session.commit()

      return jsonify(
         message = "Sign up successfully!"
      ), 200
   return jsonify(
      message = "Invalidate"
   ), 200

@app.route('/logout', methods=['POST'])
@login_required
def logout():
   if current_user.is_authenticated:
      logout_user()
      resp = jsonify({'logout': True})
      # unset_jwt_cookies(resp)
      return resp, 200

@app.route('/forgot', methods=['GET', 'POST'])
def forgot():
   if request.method == 'POST':
      sEmail = request.form['email']
      new_user = Users.query.with_entities(Users.id).filter(Users.email == sEmail).first()

      token = s.dumps({'user_id' : new_user.id}).decode('utf-8')

      # datetime object containing current date and time
      now = datetime.now()
      # dd/mm/YY H:M:S
      dDateNow = now.strftime("%d/%m/%Y %H:%M:%S")
      if Tokens.query.filter(Tokens.user_id == new_user.id, Tokens.action == 'reset-password').first():
         update_token = Tokens.query.filter(Tokens.user_id == new_user.id, Tokens.action == 'reset-password').\
            update(dict(code = token, created = dDateNow, status  = 'created'))
      else:
         db_token = Tokens(new_user.id, 'reset-password', token, dDateNow)
         db.session.add(db_token)
      db.session.commit()

      msg = Message('Confirm Email', sender = 'a06204995@gmail.com', recipients = [sEmail])

      link = url_for('reset_password', token=token, _external=True)

      msg.body = 'If you don’t use this link within 1 hours, it will expire. To get a new password reset link, visit: {}'.format(link)
      mail.send(msg)
      return jsonify(
         message = 'Check your email for a link to reset your password. If it doesn’t appear within a few minutes, check your spam folder.'
      ), 200
   return render_template('client/forgot.html')

@app.route('/reset-password/<token>')
def reset_password(token):
   try:
      id = s.loads(token)['user_id']
      new_token = Tokens.query.filter(Tokens.user_id == id, Tokens.action == 'reset-password').first()
      if new_token:
         if new_token.status == 'finish':   return render_template('client/message.html', message = 'The token is expired!')
         # datetime object containing current date and time
         now = datetime.now()
         # dd/mm/YY H:M:S
         dDateNow = datetime.strptime(now.strftime("%d/%m/%Y %H:%M:%S"), "%d/%m/%Y %H:%M:%S")

         dCreated = datetime.strptime(new_token.created, "%d/%m/%Y %H:%M:%S")
         time = dDateNow - dCreated
         if time.total_seconds() > 3600:
            return render_template('client/message.html', message = 'The token is expired!')
      else: return render_template('client/message.html', message = 'The token is expired!')
   except SignatureExpired:
      return render_template('client/message.html', message = 'The token is expired!')
   return render_template('client/reset_password.html', token=token)

@app.route('/change-password', methods=['POST'])
def change_password():
   sPassword = request.form['password']
   sConfirm = request.form['confirm']
   token = request.form['token']
   try:
      id = s.loads(token)['user_id']
   except SignatureExpired:
      return '<h1>The token is expired!</h1>'
   if sPassword != sConfirm:
      return jsonify(
         message = 'validate'
      ), 200

   # datetime object containing current date and time
   now = datetime.now()
   # dd/mm/YY H:M:S
   dDateNow = now.strftime("%d/%m/%Y %H:%M:%S")
   
   new_user = Users.query.\
               filter(Users.id == id).\
                  update(dict(password = generate_password_hash(sPassword, method='sha256'), modified = dDateNow))
   update_token = Tokens.query.filter(Tokens.user_id == id, Tokens.action == 'reset-password').\
            update(dict(created = dDateNow, status = 'finish'))
   db.session.commit()
   return jsonify(
      message = 'Password is changed successfully'
   ), 200

@app.route('/comment', methods=['POST'])
@jwt_required()
def comment():
   sContent = request.form['content']
   sBookId = request.form['book-id']

   oUser = Users.query.with_entities(Users.id).\
            filter(Users.username == str(get_jwt_identity())).first()

   # datetime object containing current date and time
   now = datetime.now()
   # dd/mm/YY H:M:S
   dDateNow = now.strftime("%d/%m/%Y %H:%M:%S")

   new_comment = Comments(oUser.id, sBookId, sContent, dDateNow)

   db.session.add(new_comment)
   db.session.commit()

   return jsonify(
      message = "Comment successfully!"
   ), 200

@app.route('/get-comment', methods=['POST'])
def getComment():
   sId = request.form['id']
   aComment = Comments.query.join(Users, Comments.user_id == Users.id).\
      with_entities(Comments.content, Comments.created, Users.firstname, Users.lastname).\
         filter(Comments.book_id == sId).all()
   
   aJsonComment = []
   for oComment in aComment:
      aJsonComment.append({
         'firstname' : oComment.firstname,
         'lastname' : oComment.lastname,
         'content' : oComment.content,
         'created' : oComment.created
      })
   return jsonify(
      comments = aJsonComment
   ), 200

@app.route('/get-info')
@jwt_required()
def get_info():
   new_user = Users.query.\
      with_entities(Users.firstname, Users.lastname, Users.username, Users.address, Users.phone_number, Users.money, Users.email).\
         filter(Users.username == str(get_jwt_identity())).first()
   return jsonify(
      firstname = new_user.firstname,
      lastname = new_user.lastname,
      username = new_user.username,
      address = new_user.address,
      phone = new_user.phone_number,
      money = new_user.money,
      email = new_user.email
   ), 200

@app.route('/change-info', methods=['POST'])
@jwt_required()
def change_info():
   sLastname = request.form['lastname']
   sFirstname = request.form['firstname']
   sEmail = request.form['email']
   sAddress = request.form['address']
   sPhone = request.form['phone']
   sMoney = request.form['money']

   if sLastname == '' or sFirstname == '' or sEmail == '' or sAddress == '' or sPhone == '' or fl(sMoney) < 0:
      return jsonify(
         message = 'invalid'
      ), 200
   
   new_user = Users.query.filter(Users.username == str(get_jwt_identity())).\
      update(dict(firstname=sFirstname, lastname=sLastname, email=sEmail, address=sAddress, phone_number=sPhone, money=str(round(float(sMoney), 2))))
   db.session.commit()
   return jsonify(
      message = 'Changed successfully'
   ), 200

@app.route('/check-login', methods=['POST'])
def check_login():
   if current_user.is_authenticated:
      login = True
   else:
      login = False
   return jsonify(login = login), 200

if __name__ == '__main__':
    app.run()
