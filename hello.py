from flask import Flask, render_template, request, redirect, url_for, make_response

from db_util import Database
from help_function import get_products_from_db, get_sets_from_db, get_toys

app = Flask(__name__, static_folder='./static')

app.secret_key = "111"

db = Database()


# menu
@app.route("/")
def products_list():
    return redirect(url_for('menu'), 301)


@app.route("/menu")
def menu(user=''):
    context = get_products_from_db(user)
    return render_template("main.html", **context)


# registration
@app.route("/menu/registration/", methods=['GET', 'POST'])
def registration():
    error = ''
    email, name, second_name, birthday, phone = '', '', '', '', ''
    if request.method == 'POST':
        email = request.form.get('email')
        name = request.form.get('name')
        second_name = request.form.get('second-name')
        birthday = request.form.get('birthday')
        phone = request.form.get('phone')
        password = request.form.get('psw')
        rep_password = request.form.get('psw-repeat')
        id = db.last_id('client') + 1
        if password != rep_password:
            error = 'Пароли не совпадают'
        elif ('@' not in email or '.' not in email) and email != 'admin':
            error = 'Логин не верный'
        elif birthday >= '2020-12-31':
            error = 'Дата не верна'
        if not error:
            a = (id, email, name, second_name, birthday, password, phone)
            db.insert('client', a)
            res = make_response("")
            res.set_cookie("user", email, 60 * 60 * 24 * 15)
            res.headers['location'] = url_for('menu')
            return res, 302
        context = {'error': error,
                   'email': email,
                   'name': name,
                   'second_name': second_name,
                   'birthday': birthday,
                   'phone': phone}
        return render_template("registration.html", **context)
    context = {'error': error,
               'email': email,
               'name': name,
               'second_name': second_name,
               'birthday': birthday,
               'phone': phone}
    return render_template("registration.html", **context)


# login
@app.route("/menu/login/", methods=['POST', 'GET'])
def login():
    error, email = '', ''
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('psw')
        clients = db.select_all('client')
        for client in clients:
            if client['email'] == email and client['password'] == password:
                res = make_response("")
                res.set_cookie("user", email, 60 * 60 * 24 * 15)
                res.headers['location'] = url_for('menu')
                return res, 302
        error = 'Неверные пароль или логин'
        context = {'error': error,
                   'email': email}
        return render_template("login.html", **context)
    context = {'error': error,
               'email': email}
    return render_template("login.html", **context)


# logout
@app.route("/menu/logout/")
def logout():
    res = make_response("Cookie Removed")
    email = request.cookies.get('user')
    res.set_cookie('user', email, max_age=0)
    res.headers['location'] = url_for('menu')
    return res, 302


# toys
@app.route("/menu/toys/")
def toys():
    context = get_toys()
    return render_template("toys.html", **context)


# sets
@app.route("/menu/sets/")
def sets():
    context = get_sets_from_db('Новогодний набор')
    return render_template("sets.html", **context)


# process
@app.route("/menu/process/")
def process():
    contex = get_sets_from_db("Процесс")
    return render_template("process.html", **contex)


# product
@app.route("/menu/<int:product_id>", methods=['POST', 'GET'])
def get_product(product_id):
    product = db.select('id', product_id, 'products')
    # if request.method == 'post':
    #     if request.cookies.get('backet') and request.form['index'] == 'backet':
    #         backet = request.cookies.get('backet').append(product_id)
    #         res = make_response("")
    #         res.set_cookie("backet", backet, 60 * 60 * 24 * 15)
    #         res.headers['location'] = url_for('menu')
    #         return res, 302
    #     else:
    #         backet = [product_id]
    #         res = make_response("")
    #         res.set_cookie("backet", backet, 60 * 60 * 24 * 15)
    #         res.headers['location'] = url_for('menu')
    #         return res, 302
    if len(product):
        return render_template("product.html", title=product['name'], product=product)

    # если нужный фильм не найден, возвращаем шаблон с ошибкой
    return render_template("error.html", error="Такой игрушки не существует в системе")


@app.route("/menu/<int:product_id>/del/", methods=['POST', 'GET'])
def del_product(product_id):
    product = db.select('id', product_id, 'products')
    id = product['id']
    db.update('products', id, 'status', 'False')
    return redirect(url_for('get_product', product_id=id), 301)


@app.route("/menu/<int:product_id>/restart_product/", methods=['POST', 'GET'])
def restart_product(product_id):
    product = db.select('id', product_id, 'products')
    id = product['id']
    db.update('products', id, 'status', 'True')
    return redirect(url_for('get_product', product_id=id), 301)


@app.route("/menu/add_product/", methods=['POST', 'GET'])
def add_product():
    error = ''
    name, discription, price, picture= '', '', '', ''
    if request.method == 'POST':
        name = request.form.get('name')
        picture = request.form.get('picture')
        price = request.form.get('price')
        discription = request.form.get('discription')
        id = db.last_id('products') + 1
        if not name:
            error = 'Поле название не заполнено'
        elif not discription:
            error = 'Поле описание не заполнено'
        elif not price:
            error = 'Поле цена не заполнено'
        elif not picture:
            error = 'Поле картинка не заполнено'
        if not error:
            a = (id, name, discription, price, picture)
            db.insert('products', a)
            return redirect(url_for('menu'), 301)
    context = {'error': error,
                   'discription': discription,
                   'name': name,
                   'price': price,
                   'picture': picture}
    return render_template("product_add.html", **context)


@app.route("/menu/<int:product_id>/reduct_product/", methods=['POST', 'GET'])
def reduct_product(product_id):
    error = ''
    product = db.select('id', product_id, 'products')
    id = product['id']
    if request.method == 'POST':
        name = request.form.get('name')
        discription = request.form.get('discription')
        price = request.form.get('price')
        picture = request.form.get('picture')
        if not error:
            if name != product['name']:
                db.update('products', id, 'name', name)
            if discription != product['discription']:
                db.update('products', id, 'discription', discription)
            if price != product['price']:
                db.update_int('products', id, 'price', price)
            if picture != product['picture']:
                db.update('products', id, 'picture', picture)
            return redirect(url_for('get_product', product_id=id), 301)
        return render_template("reduct_product.html", product=product, error=error)
    return render_template("reduct_product.html", product=product, error=error)


# backet
@app.route("/menu/backet/")
def backet():
    product = request.cookies.get('backet')


# like
@app.route("/menu/like/")
def like():
    product = request.cookies.get('backet')


# profil
@app.route("/menu/profil/", methods=['POST', 'GET'])
def profil():
    email = request.cookies.get('user')
    user = db.select('email', email, 'client')
    if request.method=='POST':
        return redirect(url_for('reduct_profil'), 301)
    return render_template("profil.html", user=user)


@app.route("/menu/reduct_profil/", methods=['POST', 'GET'])
def reduct_profil():
    error = ''
    email = request.cookies.get('user')
    user = db.select('email', email, 'client')
    id = user['id']
    if request.method=='POST':
        email = request.form.get('email')
        name = request.form.get('name')
        second_name = request.form.get('second-name')
        birthday = request.form.get('birthday')
        phone = request.form.get('phone')
        if ('@' not in email or '.' not in email) and email != 'admin':
            error = 'Логин не верный'
        elif birthday >= '2020-12-31':
            error = 'Дата не верна'
        if not error:
            if name != user['name']:
                db.update('client', id, 'name', name)
            if second_name != user['second_name']:
                db.update('client', id, 'second_name', second_name)
            if birthday != user['birthday']:
                db.update('client', id, 'birthday', birthday)
            if phone != user['phone']:
                db.update('client', id, 'phone', phone)
            if email != user['email']:
                db.update('client', id, 'email', email)
                res = make_response("")
                res.set_cookie("user", email, 60 * 60 * 24 * 15)
                res.headers['location'] = url_for('profil')
                return res, 302
            return redirect(url_for('profil'), 301)
        return render_template("reduct_profil.html", user=user, error=error)
    return render_template("reduct_profil.html", user=user, error=error)
