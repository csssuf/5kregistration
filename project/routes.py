from project import app
from project.views import core

def add_url_routes(routes_tuple):
    for route, view_function in routes_tuple:
        app.add_url_rule(route, view_function.__name__, view_function,
                methods=["GET", "POST"])

add_url_routes((
    ('/', core.index),
    ('/index', core.index)
))
