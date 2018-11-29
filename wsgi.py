# wsgi.py
import os
import logging
#logging.warn(os.environ["DUMMY"])
from flask import Flask, request
from config import Config
app = Flask(__name__)
app.config.from_object(Config)

from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow # Order is important here!
db = SQLAlchemy(app)
ma = Marshmallow(app)
from models import Product
from schemas import products_schema, product_schema

@app.route('/hello')
def hello():
    return "Hello World!"

@app.route('/products', methods=['GET', 'POST'])
def products():
    if request.method == 'GET':
        products = db.session.query(Product).all() # SQLAlchemy request => 'SELECT * FROM products'
        return products_schema.jsonify(products)

    product = Product()
    newprod = request.get_json()
    product.name = newprod['name']
    db.session.add(product)
    db.session.commit()
    return product_schema.jsonify(product), 201

@app.route('/products/<int:product_id>', methods=['GET', 'DELETE', 'PATCH'])
def product(product_id):
    product = db.session.query(Product).get(product_id)
    if product == None:
        return '{ "message": "not found"}', 404

    if request.method == 'GET':
        return product_schema.jsonify(product), 200
    elif request.method == 'DELETE':
        db.session.delete(product)
        db.session.commit()
        return '', 204
    elif request.method == 'PATCH':
        data = request.get_json()
        if data['name'] == '':
            return '', 422
        product.name = data['name']
        db.session.query(Product).commit()
        return product_schema.jsonify(product), 201
        #status.HTTP_204_NO_CONTENT


