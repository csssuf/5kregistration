from project import app
from flask import redirect
from project.views import core, register, admin

def add_url_routes(routes_tuple):
    for route, view_function in routes_tuple:
        app.add_url_rule(route, view_function.__name__, view_function,
                methods=["GET", "POST"])

add_url_routes((
    ('/', core.index),
    ('/register/', register.reg),
    ('/verify/', register.verify),
    ('/billing/<int:uid>/', register.billing),
    ('/billing/', lambda : redirect('/')),
    ('/pay/<int:uid>/', register.pay),
    ('/admin/listusers/', admin.listusers),
    ('/admin/login/', admin.login),
    ('/admin/login/login/', admin.login_form)
))
