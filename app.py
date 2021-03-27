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
from itsdangerous import Serializer, TimedJSONWebSignatureSerializer 

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
   
@app.route('/signin', methods=['GET', 'POST'])
def signin():
   if request.method == 'POST':
      sUsername = request.form['i-username']
      sPassword = request.form['i-password']
      user = Users.query.filter(Users.username == sUsername).first()
      if user:
         if check_password_hash(user.password, sPassword):
               login_user(user)
               access_token = create_access_token(identity=sUsername)
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
   if sPassword == sConfirm:
      return jsonify(
         message = "validate"
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
      message = "validate"
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

      msg = Message('Confirm Email', sender = 'a06204995@gmail.com', recipients = [sEmail])

      link = url_for('reset_password', token=token, _external=True)

      msg.body = 'If you don’t use this link within 1 hours, it will expire. To get a new password reset link, visit: {}'.format(link)
      mail.send(msg)
      return jsonify(
         message = 'Check your email for a link to reset your password. If it doesn’t appear within a few minutes, check your spam folder.'
      )
   return render_template('client/forgot.html')

@app.route('/reset-password/<token>')
def reset_password(token):
   try:
      id = s.loads(token)['user_id']
   except SignatureExpired:
      return '<h1>The token is expired!</h1>'
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
      )
   new_user = Users.query.\
               filter(Users.id == id).\
                  update(dict(password = generate_password_hash(sPassword, method='sha256')))
   db.session.commit()
   return jsonify(
      message = 'Password is changed successfully'
   )

   
if __name__ == '__main__':
    app.run()
