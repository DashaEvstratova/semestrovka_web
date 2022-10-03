# необходимые импорты
import json
from flask import Flask, render_template, request


# инициализируем приложение
# из документации:
#     The flask object implements a WSGI application and acts as the central
#     object.  It is passed the name of the module or package of the
#     application.  Once it is created it will act as a central registry for
#     the view functions, the URL rules, template configuration and much more.
app = Flask(__name__)

# дальше реализуем методы, которые мы можем выполнить из браузера,
# благодаря указанным относительным путям


# метод, который возвращает список фильмов по относительному адресу /films
@app.route("/films")
def films_list():
    # читаем файл с фильмами
    with open("films.json", 'r') as f:
        films = json.load(f)

    # получаем GET-параметр country (Russia/USA/French)
    country = request.args.get("country")
    rating = request.args.get("rating")

    # формируем контекст, который мы будем передавать для генерации шаблона
    context = {
        'films': films,
        'title': "FILMS",
        'country': country,
        'rating': rating,
    }

    # возвращаем сгенерированный шаблон с нужным нам контекстом
    return render_template("films.html", **context)

@app.route("/film/new_film", methods=['GET', 'POST'])
def put_film():
    with open("films.json", 'r') as f:
        films = json.load(f)
    if request.method == 'POST':
        film = request.form.get('film')
        country = request.form.get('country')
        rating = request.form.get('rating')
        id = films[-1]['id'] + 1
        a = dict()
        a['id'] = id
        a['name'] = film
        a['rating'] = rating
        a['country'] = country
        films.append(a)
        with open("films.json", 'w') as f:
            json.dump(films, f)
    return render_template("put_film.html")

# метод, который возвращает конкретный фильмо по id по относительному пути /film/<int:film_id>,
# где film_id - id необходимого фильма
@app.route("/film/<int:film_id>")
def get_film(film_id):
    # читаем файл
    with open("films.json", 'r') as f:
        films = json.load(f)

    # ищем нужный нам фильм и возвращаем шаблон с контекстом
    for film in films:
        if film['id'] == film_id:
            return render_template("film.html", title=film['name'], film=film)

    # если нужный фильм не найден, возвращаем шаблон с ошибкой
    return render_template("error.html", error="Такого фильма не существует в системе")