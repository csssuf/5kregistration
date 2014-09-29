from functools import wraps
from flask import session, redirect, flash

def admin_login_required(f):
    @wraps(f)
    def wrapped_f(*args, **kwargs):
        if 'admin_id' in session:
            return f(*args, **kwargs)
        flash("Admin access required to view this page.", "danger")
        return redirect('/admin/login/')
    return wrapped_f

def superadmin_login_required(f):
    @wraps(f)
    def wrapped_f(*args, **kwargs):
        if 'admin_id' in session and session['superadmin']:
            return f(*args, **kwargs)
        flash("Superadmin access required to view this page.", "danger")
        if 'admin_id' in session:
            return redirect('/admin/')
        return redirect('/admin/login/')
    return wrapped_f
