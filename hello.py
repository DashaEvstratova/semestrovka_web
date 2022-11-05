from flask import Flask, render_template, request, redirect, url_for, make_response

from db_util import Database
from help_function import get_products_from_db, get_sets_from_db

app = Flask(__name__, static_folder='./static')

app.secret_key = "111"

db = Database()


@app.route("/")
def products_list():
    return redirect(url_for('menu'), 301)


@app.route("/menu")
def menu(user=''):
    context = get_products_from_db(user)
    return render_template("main.html", **context)


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


@app.route("/menu/logout/")
def logout():
    res = make_response("Cookie Removed")
    email = request.cookies.get('user')
    res.set_cookie('user', email, max_age=0)
    res.headers['location'] = url_for('menu')
    return res, 302


@app.route("/menu/toys/")
def toys():
    context = get_products_from_db()
    return render_template("toys.html", **context)


@app.route("/menu/sets/")
def sets():
    context = get_sets_from_db('Новогодний набор')
    return render_template("sets.html", **context)


@app.route("/menu/process/")
def process():
    contex = get_sets_from_db("Процесс")
    return render_template("process.html", **contex)

@app.route("/menu/<int:product_id>", methods=['POST', 'GET'])
def get_product(product_id):
    product = db.select('id', product_id, 'products')
    if request.method == 'post':
        if request.cookies.get('backet') and request.form['index'] == 'backet':
            backet = request.cookies.get('backet').append(product_id)
            res = make_response("")
            res.set_cookie("backet", backet, 60 * 60 * 24 * 15)
            res.headers['location'] = url_for('menu')
            return res, 302
        else:
            backet = [product_id]
            res = make_response("")
            res.set_cookie("backet", backet, 60 * 60 * 24 * 15)
            res.headers['location'] = url_for('menu')
            return res, 302


    if len(product):
        return render_template("product.html", title=product['name'], product=product)

    # если нужный фильм не найден, возвращаем шаблон с ошибкой
    return render_template("error.html", error="Такой игрушки не существует в системе")


@app.route("/menu/backet/")
def backet():
    product = request.cookies.get('backet')


@app.route("/menu/profil/")
def profil():
    email = request.cookies.get('user')
    user = db.select('email', email, 'client')
    return render_template("profil.html", user=user)


#
# @app.route("/change", methods=['POST',  'GET'])
# def change():
#     if request.method == 'POST':
#         resp = make_response(redirect(url_for('films_list')))
#         userInput = request.form.get("uI")
#         if userInput == 'True':
#             resp.set_cookie('theme', 'night')
#         else:
#             resp.set_cookie('theme', 'day')
#         return resp
#     return render_template('articla.html')

# @app.route("/film/new_film", methods=['GET', 'POST'])
# def put_film():
#     if request.method == 'POST':
#         film = request.form.get('film')
#         country = request.form.get('country')
#         rating = request.form.get('rating')
#         id = db.last_id() + 1
#         a = (id, film, rating, country)
#         db.insert(a)
#
#     return render_template("put_film.html")
#
# # метод, который возвращает конкретный фильмо по id по относительному пути /film/<int:film_id>,
# # где film_id - id необходимого фильма
# @app.route("/film/<int:film_id>")
# def get_film(film_id):
#     # используем метод-обертку для выполнения запросов к БД
#     film = db.select('id', film_id)
#
#     if len(film):
#         return render_template("film.html", title=film['name'], film=film)
#
#     # если нужный фильм не найден, возвращаем шаблон с ошибкой
#     return render_template("error.html", error="Такого фильма не существует в системе")
