from flask import Flask, render_template, request, redirect, url_for

from db_util import Database

app = Flask(__name__, static_folder='./static')

app.secret_key = "111"

db = Database()


@app.route("/")
def products_list():
    return redirect(url_for('menu'), 301)


@app.route("/menu")
def menu():
    products = db.select_all('products')
    context = {
        'products': products,
    }
    return render_template("main.html", **context)

@app.route("/menu/registration/", methods=['GET', 'POST'])
def registration():
    error = ''
    if request.method == 'POST':
        email = request.form.get('email')
        name = request.form.get('name')
        second_name = request.form.get('second-name')
        birthday = request.form.get('birthday')
        phone = request.form.get('phone')
        password = request.form.get('psw')
        rep_password = request.form.get('psw-repeat')
        id = db.last_id('client') + 1
        if password == rep_password and ('@' in email and '.' in email):
            a = (id, email, name, second_name, birthday, password, phone)
            db.insert('client', a)
            message = {'message': f'Регистрация прошла успешно'}
            return render_template("reg.html", **message)
        if password != rep_password:
            return render_template("registration.html", error = 'Пароли не совпадают')
        if '@' in email or '.' in email:
            return render_template("registration.html", error='Логины не совпадают')
    return render_template("registration.html")


@app.route("/menu/login/")
def login():
    return render_template("login.html")
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
#
# @app.route("/add_cookie")
# def add_cookie():
#     resp = make_response("Add cookie")
#     resp.set_cookie("test", "val")
#     return resp
#
#
# # метод для удаления куки
# @app.route("/delete_cookie")
# def delete_cookie():
#     resp = make_response("Delete cookie")
#     resp.set_cookie("test", "val", 0)
#
#
# # реализация визитов
# @app.route("/visits")
# def visits():
#     visits_count = session['visits'] if 'visits' in session.keys() else 0
#     session['visits'] = visits_count + 1
#
#     return f"Количество визитов: {session['visits']}"
#
# @app.route("/delete_visits")
# def delete_visits():
#     session.pop('visits')
#     return "ok"

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
