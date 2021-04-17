from flask import Blueprint, render_template, request, jsonify, abort, flash, redirect
from slugify import slugify
from datetime import datetime
from models import *
from flask_sqlalchemy import SQLAlchemy
from init import db
from flask_login import current_user
from sqlalchemy import or_
import json
from flask_jwt_extended import (
    JWTManager, create_access_token, create_refresh_token,
    set_access_cookies, set_refresh_cookies,
     jwt_required,
    get_jwt_identity, unset_jwt_cookies
)

import os
from werkzeug.utils import secure_filename

ALLOWED_EXTENSIONS = set(['jpg', 'jpeg', 'png'])
  
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

book = Blueprint('book', __name__, static_folder='static', template_folder='templates')

@book.route('/<string:slug>')
def index(slug):
   oBook = Books.query.with_entities(Books.title, Books.id).filter(Books.slug == slug).first()
   return render_template('client/bookDetail.html', book=oBook, user=current_user)

@book.route('/get-all-book', methods=['POST'])
def getAllBook():
    page_num = request.form['page_num']
    order_by = request.form['order_by']
    if page_num == '' or order_by == '':
        abort(404)
    if order_by == 'desc':
        aBook =Books.query.order_by(Books.created.desc()).\
                paginate(per_page=6, page=int(page_num), error_out=True)
    elif order_by == 'asc':
        aBook =Books.query.order_by(Books.created.asc()).\
                paginate(per_page=6, page=int(page_num), error_out=True)
    else:
        abort(404)

    aJsonBook = []
    for oBook in aBook.items:
        aWriter = books_writers.query.\
            join(Writers, books_writers.writer_id == Writers.id).\
                with_entities(Writers.name, Writers.slug).filter(books_writers.book_id == oBook.id).all()
        
        aJsonWriter = []
        for oWriter in aWriter:
            aJsonWriter.append({
                'name' : oWriter.name,
                'slug' : oWriter.slug
            })

        aJsonBook.append({
            'id' : oBook.id,
            'category' : oBook.category,
            'title' : oBook.title,
            'writer' : aJsonWriter,
            'slug' : oBook.slug,
            'image' : oBook.image,
            'info' : oBook.info,
            'price' : oBook.price,
            'publisher' : oBook.publisher,
            'publish_date' : oBook.publish_date,
            'pages' : oBook.pages,
            'number' : oBook.number,
            'created' : oBook.created,
            'modified' : oBook.modified
        })
    return jsonify(
        items = aJsonBook,
        pages = aBook.pages,
        current_page = aBook.page,
        prev_num = aBook.prev_num,
        next_num = aBook.next_num
    ), 200

@book.route('/get-book-by-category', methods=['POST'])
def getBookByCategory():
    page_num = request.form['page_num']
    order_by = request.form['order_by']
    category = request.form['category']
    if page_num == '' or order_by == '' or category == '':
        abort(404)
    if order_by == 'desc':
        aBook =Books.query.filter(Books.category == category).\
        order_by(Books.created.desc()).\
            paginate(per_page=6, page=int(page_num), error_out=True)
    elif order_by == 'asc':
        aBook =Books.query.filter(Books.category == category).\
        order_by(Books.created.asc()).\
            paginate(per_page=6, page=int(page_num), error_out=True)
    else:
        abort(404)

    
    aJsonBook = []
    for oBook in aBook.items:
        aWriter = books_writers.query.\
            join(Writers, books_writers.writer_id == Writers.id).\
                with_entities(Writers.name, Writers.slug).filter(books_writers.book_id == oBook.id).all()
        
        aJsonWriter = []
        for oWriter in aWriter:
            aJsonWriter.append({
                'name' : oWriter.name,
                'slug' : oWriter.slug
            })

        aJsonBook.append({
            'title' : oBook.title,
            'writer' : aJsonWriter,
            'slug' : oBook.slug,
            'image' : oBook.image,
            'price' : oBook.price
        })
    return jsonify(
        items = aJsonBook,
        pages = aBook.pages,
        current_page = aBook.page,
        prev_num = aBook.prev_num,
        next_num = aBook.next_num
    ), 200

def get_book(aBook):
   aJsonBook = []
   for oBook in aBook.items:
      aWriter = books_writers.query.\
            join(Writers, books_writers.writer_id == Writers.id).\
               with_entities(Writers.name, Writers.slug).filter(books_writers.book_id == oBook.id).all()
      
      aJsonWriter = []
      for oWriter in aWriter:
         aJsonWriter.append({
            'name' : oWriter.name,
            'slug' :  oWriter.slug
         })

      aJsonBook.append({
        'title' : oBook.title,
        'writer' : aJsonWriter,
        'slug' : oBook.slug,
        'image' : oBook.image,
        'price' : oBook.price
      })
   return aJsonBook

@book.route('/search', methods=['POST'])
def search():
    page_num = request.form['page_num']
    value = request.form['value']
    search_by = request.form['search_by']
    if page_num == '' or value == '' or search_by == '':
        abort(404)

    sSearchValue = "%{}%".format(value)

    if search_by == 'book':
        aBook = Books.query.\
            filter(Books.title.like(sSearchValue)).\
                paginate(per_page=6, page=int(page_num), error_out=True)
        aJsonBook = get_book(aBook)

        return jsonify(
            items = aJsonBook,
            pages = aBook.pages,
            current_page = aBook.page,
            prev_num = aBook.prev_num,
            next_num = aBook.next_num
        ), 200
    elif search_by == 'author':
        aBook = books_writers.query.\
            join(Books, books_writers.book_id == Books.id).\
                join(Writers, books_writers.writer_id == Writers.id).\
                    with_entities(Books.image, Books.title, Books.price, Books.slug, Books.id).\
                        filter(Writers.name.like(sSearchValue)).\
                            paginate(per_page=6, page=int(page_num), error_out=True)
        aJsonBook = get_book(aBook)

        return jsonify(
            items = aJsonBook,
            pages = aBook.pages,
            current_page = aBook.page,
            prev_num = aBook.prev_num,
            next_num = aBook.next_num
        ), 200
    elif search_by == 'all':
        aBook = books_writers.query.\
            join(Books, books_writers.book_id == Books.id).\
                join(Writers, books_writers.writer_id == Writers.id).\
                    with_entities(Books.image, Books.title, Books.price, Books.slug, Books.id).\
                        filter(or_(Writers.name.like(sSearchValue), Books.title.like(sSearchValue))).\
                            paginate(per_page=6, page=int(page_num), error_out=True)
        aJsonBook = get_book(aBook)

        return jsonify(
            items = aJsonBook,
            pages = aBook.pages,
            current_page = aBook.page,
            prev_num = aBook.prev_num,
            next_num = aBook.next_num
        ), 200
    else:
        abort(404)

@book.route('/get-detail-book', methods=['POST'])
def getDetail():
    sId = request.form['id']
    oBook = Books.query.filter(Books.id == sId).first()
    aWriter = books_writers.query.\
            join(Writers, books_writers.writer_id == Writers.id).\
                with_entities(Writers.name, Writers.slug).filter(books_writers.book_id == oBook.id).all()

    aCategory = Categories.query.with_entities(Categories.name).filter(Categories.slug == oBook.category).first()

    aJsonBook = []
    aJsonWriter = []
    for oWriter in aWriter:
        aJsonWriter.append({
            'name' : oWriter.name,
            'slug' : oWriter.slug
        })

    return jsonify(
        id = oBook.id,
        category = aCategory.name,
        title = oBook.title,
        writer = aJsonWriter,
        slug = oBook.slug,
        image = oBook.image,
        info = oBook.info,
        price = oBook.price,
        publisher = oBook.publisher,
        publish_date = oBook.publish_date,
        pages = oBook.pages,
        number = oBook.number,
        created = oBook.created,
        modified = oBook.modified,
        slug_category = oBook.category
    ), 200

@book.route('/get-book-by-author', methods=['POST'])
def getBookByAuthor():
    sWriterId = request.form['writer_id']
    sPageNum = request.form['page_num']
    aBook = Books.query.\
        join(books_writers, Books.id == books_writers.book_id).\
            filter(books_writers.writer_id == sWriterId).\
                with_entities(Books.image, Books.title, Books.price, Books.slug, Books.id).\
                    paginate(per_page=3, page=int(sPageNum), error_out=True)
    aJsonBook = []
    for oBook in aBook.items:
        aWriter = books_writers.query.\
                join(Writers, books_writers.writer_id == Writers.id).\
                with_entities(Writers.name, Writers.slug).filter(books_writers.book_id == oBook.id).all()
        
        aJsonWriter = []
        for oWriter in aWriter:
            aJsonWriter.append({
                'name' : oWriter.name,
                'slug' :  oWriter.slug
            })

        aJsonBook.append({
            'title' : oBook.title,
            'writer' : aJsonWriter,
            'slug' : oBook.slug,
            'image' : oBook.image,
            'price' : oBook.price
        })
    return jsonify(
        items = aJsonBook,
        pages = aBook.pages,
        current_page = aBook.page,
        prev_num = aBook.prev_num,
        next_num = aBook.next_num
    ), 200


@book.route('/get-detail-book-cart', methods=['POST'])
def getDetailCart():
    sId = request.form['id']
    sCount = request.form['count']
    oBook = Books.query.filter(Books.id == sId).\
        with_entities(Books.id, Books.title, Books.image, Books.price, Books.number, Books.slug).first()
    fTotal = float(sCount) * float(oBook.price)
    aJsonBook = []
    return jsonify(
        id = oBook.id,
        title = oBook.title,
        image = oBook.image,
        price = oBook.price,
        slug = oBook.slug,
        number = oBook.number,
        count = sCount,
        total = round(fTotal, 2)
    ), 200

@book.route('/get-total-price', methods=['POST'])
def getTotal():
    aData = request.form['data']
    sCoupon = request.form['coupon']

    aJsonId = json.loads(aData)
    total = 0
    for oData in aJsonId:
        if int(oData['id']) > 0 and int(oData['count']) > 0:
            new_book = Books.query.filter(Books.id == oData['id']).\
                    with_entities(Books.price).first()
            total = float(total) + float(new_book.price) * float(oData['count'])
        else:
            return jsonify(
                message = 'Error'
            ), 200

    if sCoupon:
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
                total -= float(float(total) * float(new_coupon.percent))

    return jsonify(
        total = round(total, 2)
    ), 200

@book.route('/get-data-form', methods=['POST'])
@jwt_required()
def getDataForm():
    new_user = Users.query.with_entities(Users.group_id).filter(Users.username == get_jwt_identity()).first()
    if new_user.group_id == 'admin' or new_user.group_id == 'seller':
        aJsonCategory = []
        for oCategory in Categories.query.with_entities(Categories.name, Categories.slug).all():
            aJsonCategory.append({
                'slug' : oCategory.slug,
                'name' : oCategory.name
            })

        aJsonWriter = []
        for oWriter in Writers.query.with_entities(Writers.name, Writers.slug).all():
            aJsonWriter.append({
                'slug' : oWriter.slug,
                'name' : oWriter.name
            })
        return jsonify(
            category = aJsonCategory,
            writer = aJsonWriter
        )
    
    return jsonify(
            message = 'You do not have permission to access!'
        ), 200

@book.route('/add-book', methods=['POST'])
@jwt_required()
def addBook():
    new_user = Users.query.with_entities(Users.group_id).filter(Users.username == get_jwt_identity()).first()
    if new_user.group_id == 'admin' or new_user.group_id == 'seller':
        sWriters = request.form['writers']
        sCategory = request.form['category-name']
        sTitle = request.form['title']
        sInfo = request.form['info']
        iPrice = request.form['price']
        sPublisher = request.form['publisher']
        dPublishDate = request.form['publish_date']
        iPages = request.form['pages']
        iNumber = request.form['number']
        
        file = request.files['image']
        file.filename = slugify(sTitle) + '.jpg'  #some custom file name that you want
        
        filename = secure_filename(file.filename)

        if file and allowed_file(file.filename):
            #file.save(os.path.join(app.config['static/'], filename))
            file.save("static/images/books/"+file.filename)
        # datetime object containing current date and time
        now = datetime.now()
        # dd/mm/YY H:M:S
        dDateNow = now.strftime("%d/%m/%Y %H:%M:%S")

        oBook = Books(sCategory, sTitle, slugify(sTitle), file.filename, sInfo, str(round(float(iPrice), 2)), sPublisher, dPublishDate, iPages, iNumber, dDateNow, dDateNow )

        db.session.add(oBook)
        db.session.commit()

        aSlugWriter = sWriters.split(',')
        for sSlug in aSlugWriter:
            oWriter = Writers.query.with_entities(Writers.id).filter(Writers.slug == sSlug).first()
            oBook = Books.query.with_entities(Books.id).filter(Books.title == sTitle).first()

            new_books_writers = books_writers(oBook.id, oWriter.id)
            db.session.add(new_books_writers)
            db.session.commit()
        return jsonify(
            message = 'Add successfully!'
        ), 200
    return jsonify(
        message = 'You do not have permission to access!'
    ), 200

@book.route('/delete', methods=['DELETE'])
@jwt_required()
def delete():
    new_user = Users.query.with_entities(Users.group_id).filter(Users.username == get_jwt_identity()).first()
    if new_user.group_id == 'admin' or new_user.group_id == 'seller':
        id = request.form['id']
        oBook = Books.query.filter(Books.id == id).first()
        aBookWriter = books_writers.query.filter(books_writers.book_id == id).all()
        for oBookWriter in aBookWriter:
            db.session.delete(oBookWriter)
        os.remove("static/images/books/"+ oBook.image)
        db.session.delete(oBook)
        db.session.commit()
        return jsonify(
            message = 'Deleted successfully!'
        )
    
    return jsonify(
        message = 'You do not have permission to access!'
    ), 200

@book.route('/search-admin', methods=['POST'])
@jwt_required()
def search_admin():
    new_user = Users.query.with_entities(Users.group_id).filter(Users.username == get_jwt_identity()).first()
    if new_user.group_id == 'admin' or new_user.group_id == 'seller':
        page_num = request.form['page_num']
        value = request.form['value']
        sSearchValue = "%{}%".format(value)
        aBook = Books.query.\
                filter(Books.title.like(sSearchValue)).\
                    paginate(per_page=6, page=int(page_num), error_out=True)
        aJsonBook = []
        for oBook in aBook.items:
            aWriter = books_writers.query.\
                join(Writers, books_writers.writer_id == Writers.id).\
                    with_entities(Writers.name, Writers.slug).filter(books_writers.book_id == oBook.id).all()
            
            aJsonWriter = []
            for oWriter in aWriter:
                aJsonWriter.append({
                    'name' : oWriter.name,
                    'slug' : oWriter.slug
                })

            aJsonBook.append({
                'id' : oBook.id,
                'category' : oBook.category,
                'title' : oBook.title,
                'writer' : aJsonWriter,
                'slug' : oBook.slug,
                'image' : oBook.image,
                'info' : oBook.info,
                'price' : oBook.price,
                'publisher' : oBook.publisher,
                'publish_date' : oBook.publish_date,
                'pages' : oBook.pages,
                'number' : oBook.number,
                'created' : oBook.created,
                'modified' : oBook.modified
            })
        return jsonify(
            items = aJsonBook,
            pages = aBook.pages,
            current_page = aBook.page,
            prev_num = aBook.prev_num,
            next_num = aBook.next_num
        ), 200
    return jsonify(
        message = 'You do not have permission to access!'
    ), 200

@book.route('/edit-book', methods=['POST'])
@jwt_required()
def editBook():
    new_user = Users.query.with_entities(Users.group_id).filter(Users.username == get_jwt_identity()).first()
    if new_user.group_id == 'admin' or new_user.group_id == 'seller':
        sWriters = request.form['writers']
        sCategory = request.form['category-name']
        sInfo = request.form['info']
        iPrice = request.form['price']
        sPublisher = request.form['publisher']
        dPublishDate = request.form['publish_date']
        iPages = request.form['pages']
        iNumber = request.form['number']
        iId = request.form['id']

        # datetime object containing current date and time
        now = datetime.now()
        # dd/mm/YY H:M:S
        dDateNow = now.strftime("%d/%m/%Y %H:%M:%S")

        #delete data in table book_writers
        aBookWriter = books_writers.query.\
            filter(books_writers.book_id == iId).all()

        for oBookWriter in aBookWriter:
            db.session.delete(oBookWriter)
        db.session.commit()

        #edit data in table books
        update_book = Books.query.\
            filter(Books.id == iId).\
                update(dict(category=sCategory, info=sInfo, price=str(round(float(iPrice), 2)), publisher=sPublisher, publish_date=dPublishDate, pages=iPages, number=iNumber, modified=dDateNow))
        db.session.commit()
        #add data to table book_writers
        aSlugWriter = sWriters.split(',')
        for sSlug in aSlugWriter:
            oWriter = Writers.query.with_entities(Writers.id).filter(Writers.slug == sSlug).first()

            new_books_writers = books_writers(iId, oWriter.id)
            db.session.add(new_books_writers)
            db.session.commit()
        return jsonify(
            message = 'Edit successfully!'
        ), 200
    return jsonify(
        message = 'You do not have permission to access!'
    ), 200

@book.route('/edit-image', methods=['POST'])
@jwt_required()
def editBookImage():
    new_user = Users.query.with_entities(Users.group_id).filter(Users.username == get_jwt_identity()).first()
    if new_user.group_id == 'admin' or new_user.group_id == 'seller':
        # datetime object containing current date and time
        now = datetime.now()
        # dd/mm/YY H:M:S
        dDateNow = now.strftime("%d/%m/%Y %H:%M:%S")
        
        # delete image in dict
        id = request.form['id']
        oBook = Books.query.filter(Books.id == id).first()
        os.remove("static/images/books/"+ oBook.image)

        # add new image
        file = request.files['image']
        file.filename = oBook.slug+ '' + slugify(dDateNow) + '.jpg'  #some custom file name that you want
        
        filename = secure_filename(file.filename)

        if file and allowed_file(file.filename):
            file.save("static/images/books/"+file.filename)

        update_book = Books.query.\
            filter(Books.id == id).\
                update(dict(image=file.filename, modified=dDateNow))
        db.session.commit()
        
        return jsonify(
            message = 'Edit successfully!'
        ), 200
    return jsonify(
        message = 'You do not have permission to access!'
    ), 200