import psycopg2

class Database:
    def __init__(self):
        self.con = psycopg2.connect(
            dbname="web",
            user="postgres",
            password=1864,
            host="localhost",
            port=5432
        )
        self.cur = self.con.cursor()

    def insert(self, object):
        inserts = f"INSERT INTO films values {object};\n"
        self.cur.execute(inserts)
        self.con.commit()

    def select_all(self):
        self.cur.execute(f"SELECT * FROM films")
        return self.help_select()

    def select(self, parametr, name):
        self.cur.execute(f"SELECT * FROM films WHERE {parametr} = '{name}';")
        return self.help_select()

    def select_rating(self, rating):
        self.cur.execute(f"SELECT * FROM films WHERE rating >= {rating};")
        return self.help_select()

    def select_rating_country(self, country_, rating):
        self.cur.execute(f"SELECT * FROM films WHERE country = '{country_}' AND rating >= '{rating}';")
        return self.help_select()


    def help_select(self):
        data = self.prepare_data(self.cur.fetchall())
        if len(data) == 1:
            data = data[0]

        return data

    def prepare_data(self, data):
        films = []
        if len(data):
            column_names = [desc[0] for desc in self.cur.description]
            for row in data:
                films += [{c_name: row[key] for key, c_name in enumerate(column_names)}]

        return films

    def last_id(self):
        films = self.select_all()
        return films[-1]['id']