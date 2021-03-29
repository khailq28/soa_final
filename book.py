from flask import Blueprint, render_template, request, jsonify, abort, flash, redirect
from slugify import slugify
from datetime import datetime
from models import Books, books_writers, Writers, Categories, Coupons
from flask_sqlalchemy import SQLAlchemy
from init import db
from flask_login import current_user
from sqlalchemy import or_
import json

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
            with_entities(Books.image, Books.title, Books.price, Books.slug, Books.id).\
                paginate(per_page=6, page=int(page_num), error_out=True)
    elif order_by == 'asc':
        aBook =Books.query.order_by(Books.created.asc()).\
            with_entities(Books.image, Books.title, Books.price, Books.slug, Books.id).\
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
            paginate(per_page=8, page=int(page_num), error_out=True)
    elif order_by == 'asc':
        aBook =Books.query.filter(Books.category == category).\
        order_by(Books.created.asc()).\
            paginate(per_page=8, page=int(page_num), error_out=True)
    else:
        abort(404)

    
    aJsonBook = []
    for oBook in aBook.items:
        aWriter = books_writers.query.\
            join(Writers, books_writers.writer_id == Writers.id).\
                with_entities(Writers.name).filter(books_writers.book_id == oBook.id).all()
        
        aJsonWriter = []
        for oWriter in aWriter:
            aJsonWriter.append({
                'name' : oWriter.name
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
        modified = oBook.modified
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
    sTotal = int(sCount) * int(oBook.price)
    aJsonBook = []
    return jsonify(
        id = oBook.id,
        title = oBook.title,
        image = oBook.image,
        price = oBook.price,
        slug = oBook.slug,
        number = oBook.number,
        count = sCount,
        total = sTotal
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
            total = int(total) + int(new_book.price) * int(oData['count'])
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
                total = int(int(total) * float(new_coupon.percent))

    return jsonify(
        total = total
    ), 200

