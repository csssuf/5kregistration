from flask import render_template, request, session, flash
from project.utils.auth import admin_login_required
from project.models import Admin
import hashlib

@admin_login_required
def listusers():
    return render_template("admin_listusers.html")

def login():
    return render_template("admin_login.html")

def login_submit():
    if request.method == "POST":
        if Admin.query.filter(Admin.username == request.form["username"]).first() == None:
            flash("Invalid username or password.", "danger")
        elif Admin.query.filter((Admin.username == request.form["username"]) & (Admin.pwhash == hashlib.sha256(request.form["password"]).hexdigest())).first() == None:
            flash("Invalid username or password.", "danger")
        else:
            auser = Admin.query.filter(Admin.username == request.form["username"]).first()
            session["admin_id"] = auser.username
            session["superadmin"] = auser.superadmin
    return render_template("admin_login.html")