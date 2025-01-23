import json

import flask
import jwt
from flask import render_template, request, redirect, url_for
import products
from auth import do_login, sign_up
from products import list_products
from cart import add_to_cart as ac, get_cart, remove_from_cart, delete_cart
from checkout import checkout as chk, complete_checkout
import os
from functools import lru_cache

app = flask.Flask(__name__)
app.template_folder = 'templates'
SRN = "PES1UG22CS489"

if(SRN[-3:]=="XXX"):
    print("Please update your SRN on line 15")
    os._exit(1)

@app.route('/')
def index():
    return redirect(url_for('browse'))


@app.route('/cart')
def cart():
    token = request.cookies.get('token')
    if token is None:
        return redirect(url_for('login'))
    dec = jwt.decode(token, 'secret', algorithms=['HS256'])
    username = dec['sub']
    cart = get_cart(username)
    return render_template('cart.jinja', cart=cart,srn=SRN)

@app.route('/cart/remove/<id>', methods=['POST'])
def remove_cart_item(id):
    token = request.cookies.get('token')
    if token is None:
        return redirect(url_for('login'))
    dec = jwt.decode(token, 'secret', algorithms=['HS256'])
    username = dec['sub']
    remove_from_cart(username, id)
    return redirect(url_for('cart'))

@app.route('/cart/delete', methods=['GET'])
def delete_cart_item():
    token = request.cookies.get('token')
    if token is None:
        return redirect(url_for('login'))
    dec = jwt.decode(token, 'secret', algorithms=['HS256'])
    username = dec['sub']
    delete_cart(username)
    return redirect(url_for('cart'))

@app.route('/cart/<id>', methods=['POST'])
def add_to_cart(id):
    payload={
        "id": id
    }
    token = request.cookies.get('token')
    if token is None:
        return redirect(url_for('login'))
    dec = jwt.decode(token, 'secret', algorithms=['HS256'])
    username = dec['sub']
    print(username)
    ac(username, id)
    return redirect(url_for('cart'))


@app.route('/product/<product_id>')
def product(product_id):
    product = products.get_product(product_id)
    return flask.render_template('product_view.jinja', product=product,srn=SRN)


@app.route("/product", methods=['GET', 'POST'])
def product_page():
    if request.method == 'POST':
        print(request.form)
        product_name = request.form['product_name']
        product_cost = request.form['product_cost']
        product_quantity = request.form['product_quantity']
        product_description = request.form['product_description']
        products.add_product({"name": product_name, "cost": product_cost, "qty": product_quantity,
                              "description": product_description})
        # return "Success", 200, {"Access-Control-Allow-Origin": "*"}
        return 'ok'
    else:
        return flask.render_template('product.jinja',srn=SRN)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # handle the login form submission
        username, password = request.form['username'], request.form['password']
        try:
            token = do_login(username, password)
            resp = flask.make_response(redirect(url_for('browse')))
            resp.set_cookie('token', token)
            return resp
        except ValueError as e:
            response = flask.make_response({'error': str(e)})
            response.status_code = 401
            return response
    else:
        # render the login page with a form
        return render_template('login.jinja',srn=SRN)


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        # handle the register form submission
        username, password = request.form['username'], request.form['password']
        try:
            sign_up(username, password)
            return redirect(url_for('login'))
        except ValueError as e:
            response = flask.make_response({'error': str(e)})
            response.status_code = 400
            return response
    return render_template('signup.jinja',srn=SRN)

@lru_cache(maxsize=1)
def cached_product_list():
    return list_products()

@app.route("/browse")
def browse():
    return render_template('browse.jinja', items=cached_product_list(), srn=SRN)


@app.route("/checkout", methods=['GET', 'POST'])
def checkout():
    token = request.cookies.get('token')
    if token is None:
        return redirect(url_for('login'))
    dec = jwt.decode(token, 'secret', algorithms=['HS256'])
    username = dec['sub']
    if request.method == 'GET':
        total = chk(username)
        return render_template('checkout.jinja', total=total,srn=SRN)
    else:
        resp = flask.make_response(redirect(url_for('browse')))
        return resp

@app.route("/payment", methods=['GET'])
def payment():
    token = request.cookies.get('token')
    if token is None:
        return redirect(url_for('login'))
    dec = jwt.decode(token, 'secret', algorithms=['HS256'])
    username = dec['sub']
    complete_checkout(username)
    return render_template('payment.jinja',srn=SRN)

# Run the app
if __name__ == '__main__':
    app.run(debug=True)