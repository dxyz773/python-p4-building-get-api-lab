#!/usr/bin/env python3

from flask import Flask, make_response, jsonify
from flask_migrate import Migrate

from models import db, Bakery, BakedGood

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///app.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.json.compact = False

migrate = Migrate(app, db)

db.init_app(app)


@app.route("/")
def index():
    return "<h1>Bakery GET API</h1>"


@app.route("/bakeries")
def bakeries():
    bakery_list = []

    for bakery in Bakery.query.all():
        bakery_dict = bakery.to_dict()
        bakery_list.append(bakery_dict)

    response = make_response(jsonify(bakery_list), 200)

    return response


@app.route("/bakeries/<int:id>")
def bakery_by_id(id):
    bakery = Bakery.query.filter(Bakery.id == id).first()
    bakery_dict = bakery.to_dict()
    response = make_response(bakery_dict, 200)
    return response


@app.route("/baked_goods/by_price")
def baked_goods_by_price():
    baked_goods_list = []
    for baked_good in BakedGood.query.order_by(BakedGood.price.desc()).all():
        baked_dict = baked_good.to_dict()
        baked_goods_list.append(baked_dict)

    response = make_response(baked_goods_list, 200)
    return response


@app.route("/baked_goods/most_expensive")
def most_expensive_baked_good():
    top_good = BakedGood.query.order_by(BakedGood.price.desc()).first()
    top_dict = top_good.to_dict()

    response = make_response(jsonify(top_dict), 200)
    return response


if __name__ == "__main__":
    app.run(port=5555, debug=True)
