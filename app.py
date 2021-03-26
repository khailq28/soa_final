from flask import Flask, render_template, request, jsonify
from models import *
from admin import admin
from category import category
from book import book
from coupon import coupon
from group import group
from order import order
from writer import writer
from init import app, db
from datetime import datetime
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash

from flask_jwt_extended import (
    JWTManager, create_access_token, create_refresh_token,
    set_access_cookies, set_refresh_cookies,
     jwt_required,
    get_jwt_identity, unset_jwt_cookies
)

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
   return render_template('client/signin.html')

@app.route('/signup', methods=['POST'])
def signup():
   sLastname = request.form['lastname']
   sFirstname = request.form['firstname']
   sUsername = request.form['username']
   sPassword = request.form['password']
   sEmail = request.form['email']
   sAddress = request.form['address']
   sPhone = request.form['phone']
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
    logout_user()
    resp = jsonify({'logout': True})
    # unset_jwt_cookies(resp)
    return resp, 200

@app.route('/forgot', methods=['GET', 'POST'])
def forgot():
   return render_template('client/forgot.html')

@app.route('/search')
def searchPage():
   return render_template('search.html')

@app.route('/test')
@login_required
def test():
   return 'sss'

if __name__ == '__main__':
    app.run()
