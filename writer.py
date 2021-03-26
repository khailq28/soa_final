from flask import Blueprint, render_template, request, jsonify, abort, flash
from slugify import slugify
from datetime import datetime
from models import Writers
from flask_sqlalchemy import SQLAlchemy
from init import db
from flask_login import current_user
from sqlalchemy.sql import func

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