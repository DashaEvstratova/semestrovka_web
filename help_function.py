from db_util import Database

db = Database()

def get_products_from_db(user = ''):
    products = db.select_all('products')
    context = {
        'user':user,
        'products': products,
    }
    return context

def get_sets_from_db(name):
    products = db.select('name', name, 'products')
    context = {
        'products': products,
    }
    return context