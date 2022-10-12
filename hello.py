from flask import Flask, render_template, request, make_response, session, redirect, url_for
from db_util import Database


app = Flask(__name__, static_folder='./static')

app.secret_key = "111"

db = Database()


@app.route("/change", methods=['POST',  'GET'])
def change():
    if request.method == 'POST':
        resp = make_response(redirect(url_for('films_list')))
        userInput = request.form.get("userInput")
        if userInput == 'True':
            resp.set_cookie('theme', 'night')
        else:
            resp.set_cookie('theme', 'day')
        return resp
    return render_template('articla.html')

@app.route("/add_cookie")
def add_cookie():
    resp = make_response("Add cookie")
    resp.set_cookie("test", "val")
    return resp


# метод для удаления куки
@app.route("/delete_cookie")
def delete_cookie():
    resp = make_response("Delete cookie")
    resp.set_cookie("test", "val", 0)


# реализация визитов
@app.route("/visits")
def visits():
    visits_count = session['visits'] if 'visits' in session.keys() else 0
    session['visits'] = visits_count + 1

    return f"Количество визитов: {session['visits']}"

@app.route("/delete_visits")
def delete_visits():
    session.pop('visits')
    return "ok"

@app.route("/films")
def films_list():
    # читаем файл с фильмами
    films = db.select_all()


    # получаем GET-параметр country (Russia/USA/French)
    country = request.args.get("country")
    rating = request.args.get("rating")
    if rating and country:
        films = db.select_rating_country(country, float(rating))
    elif rating:
        films = db.select_rating(float(rating))
    elif country:
        films = db.select('country', country)

    # формируем контекст, который мы будем передавать для генерации шаблона
    context = {
        'films': films,
        'title': "FILMS",

    }

    # возвращаем сгенерированный шаблон с нужным нам контекстом
    return render_template("films.html", **context)

@app.route("/film/new_film", methods=['GET', 'POST'])
def put_film():
    if request.method == 'POST':
        film = request.form.get('film')
        country = request.form.get('country')
        rating = request.form.get('rating')
        id = db.last_id() + 1
        a = (id, film, rating, country)
        db.insert(a)

    return render_template("put_film.html")

# метод, который возвращает конкретный фильмо по id по относительному пути /film/<int:film_id>,
# где film_id - id необходимого фильма
@app.route("/film/<int:film_id>")
def get_film(film_id):
    # используем метод-обертку для выполнения запросов к БД
    film = db.select('id', film_id)

    if len(film):
        return render_template("film.html", title=film['name'], film=film)

    # если нужный фильм не найден, возвращаем шаблон с ошибкой
    return render_template("error.html", error="Такого фильма не существует в системе")
