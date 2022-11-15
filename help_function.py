from db_util import Database

db = Database()


def get_products_from_db(user=''):
    products = db.select_all('products')
    context = {
        'products': products,
    }
    return context


def get_sets_from_db(parametr, data, table):
    products = db.select(parametr, data, table)
    context = {
        'products': products,
    }
    return context


def get_toys(parametr='id', how='ASC'):
    products = db.select_not(parametr, how)
    context = {
        'products': products,
    }
    return context
