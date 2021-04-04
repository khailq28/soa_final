from init import db
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.dialects.postgresql import JSON
from flask_login import UserMixin

class Groups(db.Model):
    name = db.Column(db.String(100), primary_key=True)
    description = db.Column(db.String(255))
    created = db.Column(db.String(255), nullable=False)

    def __init__(self, name, description, created):
        self.name = name
        self.description = description
        self.created = created

class Users(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    group_id = db.Column(db.String(100), default='user')
    username = db.Column(db.String(50), unique=True)
    password = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(50), unique=True)
    firstname = db.Column(db.String(50), nullable=False)
    lastname = db.Column(db.String(50), nullable=False)
    address = db.Column(db.String(255), nullable=False)
    phone_number = db.Column(db.String(13), nullable=False)
    money = db.Column(db.String(255), nullable=False, default='0')
    created = db.Column(db.String(255), nullable=False)
    modified = db.Column(db.String(255), nullable=False)

    def __init__(self, username, password, email, firstname, lastname, address, phone_number, created, modified):
        self.username = username
        self.password = password
        self.email = email
        self.firstname = firstname
        self.lastname = lastname
        self.address = address
        self.phone_number = phone_number
        self.created = created
        self.modified = modified

class Orders(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, nullable=False)
    order_info = db.Column(JSON, nullable=False)
    payment_info = db.Column(db.String(255), nullable=False)
    status = db.Column(db.String(255), nullable=False)
    created = db.Column(db.String(255), nullable=False)
    modified = db.Column(db.String(255), nullable=False)

    def __init__(self, user_id, order_info, payment_info, status, created, modified):
        self.user_id = user_id
        self.order_info = order_info
        self.payment_info = payment_info
        self.status = status
        self.created = created
        self.modified = modified

class Coupons(db.Model):
    code = db.Column(db.String(256), primary_key=True)
    percent = db.Column(db.Float(3), nullable=False)
    description = db.Column(db.String(255))
    time_start = db.Column(db.String(255), nullable=False)
    time_end = db.Column(db.String(255), nullable=False)
    created = db.Column(db.String(255), nullable=False)
    modified = db.Column(db.String(255), nullable=False)

    def __init__(self, code, percent, description, time_start, time_end, created, modified):
        self.code = code
        self.percent = percent
        self.description = description
        self.time_start = time_start
        self.time_end = time_end
        self.created = created
        self.modified = modified

class Categories(db.Model):
    name = db.Column(db.String(100), primary_key=True)
    slug = db.Column(db.String(255), nullable=False)
    created = db.Column(db.String(255), nullable=False)
    modified = db.Column(db.String(255), nullable=False)

    def __init__(self, name, slug, created, modified):
        self.name = name
        self.slug = slug
        self.created = created
        self.modified = modified

class Books(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    category = db.Column(db.String(100), nullable=False)
    title = db.Column(db.String(100), nullable=False, unique=True)
    slug = db.Column(db.String(255), nullable=False)
    image = db.Column(db.String(255), nullable=False)
    info = db.Column(db.Text, nullable=False)
    price = db.Column(db.Integer, nullable=False)
    publisher = db.Column(db.String(100), nullable=False)
    publish_date = db.Column(db.String(100), nullable=False)
    pages = db.Column(db.Integer, nullable=False)
    number = db.Column(db.Integer, nullable=False)
    created = db.Column(db.String(255), nullable=False)
    modified = db.Column(db.String(255), nullable=False)

    def __init__(self, category, title, slug, image, info, price, publisher, publish_date, pages, number, created, modified):
        self.category = category
        self.title = title
        self.slug = slug
        self.image = image
        self.info = info
        self.price = price
        self.publisher = publisher
        self.publish_date = publish_date
        self.pages = pages
        self.number = number
        self.created =created
        self.modified =modified

class Writers(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True)
    slug = db.Column(db.String(255), nullable=False)
    biography = db.Column(db.Text, nullable=False)
    created = db.Column(db.String(255), nullable=False)
    modified = db.Column(db.String(255), nullable=False)

    def __init__(self, name, slug, biography, created, modified):
        self.name = name
        self.slug = slug
        self.biography = biography
        self.created = created
        self.modified = modified

class books_writers(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    book_id = db.Column(db.Integer, nullable=False)
    writer_id = db.Column(db.Integer, nullable=False)

    def __init__(self, book_id, writer_id):
        self.book_id = book_id
        self.writer_id = writer_id

class Comments(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, nullable=False)
    book_id = db.Column(db.Integer, nullable=False)
    content = db.Column(db.Text, nullable=False)
    created = db.Column(db.String(255), nullable=False)

    def __init__(self, user_id, book_id, content, created):
        self.user_id = user_id
        self.book_id = book_id
        self.content = content
        self.created = created

class Tokens(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, nullable=False)
    action = db.Column(db.String(255), nullable=False)
    code = db.Column(db.String(255), nullable=False)
    created = db.Column(db.String(255), nullable=False)
    status = db.Column(db.String(255), default='created')
    def __init__(self, user_id, action, code, created):
        self.user_id = user_id
        self.action = action
        self.code = code
        self.created = created






