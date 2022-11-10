import psycopg2

class Database:
    def __init__(self):
        self.con = psycopg2.connect(
            dbname="semestrovka1",
            user="postgres",
            password=1864,
            host="localhost",
            port=5432
        )
        self.cur = self.con.cursor()

    def insert(self, table, object):
        inserts = f"INSERT INTO {table} values {object};\n"
        self.cur.execute(inserts)
        self.con.commit()

    def select_all(self, table):
        self.cur.execute(f"SELECT * FROM {table} ORDER BY id")
        return self.help_select()

    def select_not(self, parametr, how):
        self.cur.execute(f"SELECT * FROM products WHERE name !='Процесс'ORDER BY {parametr} {how};")
        return self.help_select()

    def select(self, parametr, data, table):
        self.cur.execute(f"SELECT * FROM {table} WHERE {parametr} ='{data}';")
        return self.help_select()

    def select_something(self, table, parametr):
        self.cur.execute(f"SELECT {parametr} FROM {table};")
        a = self.help_select()
        res = []
        for i in a:
            res.append(i[parametr])
        return res


    def help_select(self):
        data = self.prepare_data(self.cur.fetchall())
        if len(data) == 1:
            data = data[0]
        return data

    def prepare_data(self, data):
        products = []
        if len(data):
            column_names = [desc[0] for desc in self.cur.description]
            for row in data:
                products += [{c_name: row[key] for key, c_name in enumerate(column_names)}]

        return products

    def select_max(self, table):
        self.cur.execute(f"SELECT max(id) FROM {table}")
        return self.help_select()

    def last_id(self, table):
        tables = self.select_max(table)
        return tables['max']

    def update(self, table, id, parametr, data):
        self.cur.execute(f"UPDATE {table} SET {parametr} = '{data}' WHERE id = {id};")
        self.con.commit()

    def update_int(self, table, id, parametr, data):
        self.cur.execute(f"UPDATE {table} SET {parametr} = {data} WHERE id = {id};")
        self.con.commit()