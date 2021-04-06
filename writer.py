from flask import Blueprint, render_template, request, jsonify, abort, flash
from slugify import slugify
from datetime import datetime
from models import *
from flask_sqlalchemy import SQLAlchemy
from init import db
from flask_login import current_user
from sqlalchemy.sql import func

from flask_jwt_extended import (
    JWTManager, create_access_token, create_refresh_token,
    set_access_cookies, set_refresh_cookies,
     jwt_required,
    get_jwt_identity, unset_jwt_cookies
)

writer = Blueprint('writer', __name__, static_folder='static', template_folder='templates')

@writer.route('/<string:slug>')
def index(slug):
   oWriter = Writers.query.with_entities(Writers.name, Writers.id).filter(Writers.slug == slug).first()
   return render_template('client/writerDetail.html', slug=slug, writer=oWriter, user=current_user)

@writer.route('/get-random-writer', methods=['POST'])
def getRandomWriter():
    aWriter = Writers.query.\
        with_entities(Writers.id, Writers.name, Writers.slug).\
            order_by(func.random()).limit(10).all()
    aJsonWriter = []
    for oWriter in aWriter:
        aJsonWriter.append({
            'name' : oWriter.name,
            'slug' : oWriter.slug
        })
    return jsonify(
        writer = aJsonWriter
    ), 200

@writer.route('/get-detail-writer', methods=['POST'])
def getDetailWriter():
    sId = request.form['id']
    oWriter = Writers.query.\
        with_entities(Writers.name, Writers.slug, Writers.biography).\
            filter(Writers.id == sId).first()
    return jsonify(
        name = oWriter.name,
        slug = oWriter.slug,
        biography = oWriter.biography
    ), 200

@writer.route('/get-data-writer', methods=['POST'])
def getWriters():
    page_num = request.form['page_num']
    if page_num == '':
        abort(404)
    aWriter = Writers.query.order_by(Writers.id.asc()).paginate(per_page=4, page=int(page_num), error_out=True)
    aJsonWriter = []
    for oWriter in aWriter.items:
        aJsonWriter.append({
            'id' : oWriter.id,
            'name' : oWriter.name,
            'slug' : oWriter.slug,
            'biography' : oWriter.biography,
            'created' : oWriter.created,
            'modified' : oWriter.modified
        })
    return jsonify(
        items = aJsonWriter,
        pages = aWriter.pages,
        current_page = aWriter.page,
        prev_num = aWriter.prev_num,
        next_num = aWriter.next_num
    )

@writer.route('/add-writer', methods=['POST'])
def addWriter():
    sName = request.form['name']
    sBiography = request.form['biography']
    sSlug = slugify(sName)

    # datetime object containing current date and time
    now = datetime.now()
    # dd/mm/YY H:M:S
    dDateNow = now.strftime("%d/%m/%Y %H:%M:%S")
    #create new writer
    oWriter = Writers(sName, sSlug, sBiography, dDateNow, dDateNow)

    #insert into table
    db.session.add(oWriter)
    db.session.commit()

    return jsonify(
        message = 'Writer added successfully!'
    ), 200

@writer.route('/edit', methods=['POST'])
@jwt_required()
def edit():
    new_user = Users.query.with_entities(Users.group_id).filter(Users.username == get_jwt_identity()).first()
    if new_user.group_id != 'admin':
        return jsonify(
            message = 'You do not have permission to access!'
        ), 200

    sId = request.form['id']
    sName = request.form['name']
    sBiography = request.form['biography']

    # datetime object containing current date and time
    now = datetime.now()
    # dd/mm/YY H:M:S
    dDateNow = now.strftime("%d/%m/%Y %H:%M:%S")

    oWriter = Writers.query.filter(Writers.id == sId).\
        update(dict(name = sName, slug = slugify(sName), biography = sBiography, modified = dDateNow))

    db.session.commit()
    return jsonify(
        message = 'Updated successfully!'
    ), 200

@writer.route('/delete', methods=['DELETE'])
@jwt_required()
def delete():
    new_user = Users.query.with_entities(Users.group_id).filter(Users.username == get_jwt_identity()).first()
    if new_user.group_id != 'admin':
        return jsonify(
            message = 'You do not have permission to access!'
        ), 200
    id = request.form['id']
    oWriter = Writers.query.filter(Writers.id == id).first()
    db.session.delete(oWriter)
    db.session.commit()
    return jsonify(
        message = 'Deleted successfully!'
    ), 200

@writer.route('/search', methods=['POST'])
def search():
    name = request.form['name']
    name = "%{}%".format(name)
    aWriter = Writers.query.filter(Writers.name.like(name)).all()

    aOutput = []
    for oWriter in aWriter:
        aOutput.append({
            'id' : oWriter.id,
            'name' : oWriter.name,
            'slug' : oWriter.slug,
            'biography' : oWriter.biography,
            'created' : oWriter.created,
            'modified' : oWriter.modified
        })
    return jsonify(
        items = aOutput
    ), 200

