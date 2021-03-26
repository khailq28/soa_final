from flask import Flask, render_template
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

app.register_blueprint(admin, url_prefix='/admin')
app.register_blueprint(book, url_prefix='/book')
app.register_blueprint(category, url_prefix='/category')
app.register_blueprint(coupon, url_prefix='/coupon')
app.register_blueprint(group, url_prefix='/group')
app.register_blueprint(order, url_prefix='/order')
app.register_blueprint(writer, url_prefix='/writer')

@app.route('/')
def index():
   return render_template('client/home.html')
   
@app.route('/login', methods=['GET', 'POST'])
def login():
   return render_template('client/login.html')

@app.route('/search')
def searchPage():
   return render_template('search.html')

if __name__ == '__main__':
    app.run(debug=True)
