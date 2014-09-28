from functools import wraps
from flask import session, redirect, flash

def admin_login_required(f):
    @wraps(f)
    def wrapped_f(*args, **kwargs):
        if 'admin_id' in session:
            return f(*args, **kwargs)
        flash("Admin access required to view this page.", "danger")
        return redirect('/')
    return wrapped_f
