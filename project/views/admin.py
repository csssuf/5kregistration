from flask import render_template, request, session, flash, redirect
from project.utils.auth import admin_login_required, superadmin_login_required
from project.models import Admin, RegisteredUser
from project.database import db_session
import hashlib
import datetime

@admin_login_required
def listusers():
    return render_template("admin_listusers.html",
            users=db_session.query(RegisteredUser).order_by(RegisteredUser.id), int=int)

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
	    return redirect('/admin/listusers/')
    return redirect('/admin/login/')

@admin_login_required
def aindex():
    return redirect('/admin/listusers/') # Fix me after more admin functions are written

@admin_login_required
def registerrunner():
    if request.method == "POST":
        if not ("name" in request.form and "email" in request.form and "paid" in request.form and "rtype" in request.form):
            flash("Please fill out all the fields.", "danger")
            return render_template("admin_register.html")
        if RegisteredUser.query.filter(RegisteredUser.email == request.form["email"]).first() != None:
            flash("Runner already registered.", "warning")
            return render_template("admin_register.html")
        nrunner = RegisteredUser(date = datetime.datetime.now(),
                name=request.form["name"], email=request.form["email"],
                phone=''.join(c for c in request.form["phone"] if c.isdigit()),
                paid=100*int(request.form["paid"]), verified = True,
                rtype =request.form["rtype"])
        db_session.add(nrunner)
        db_session.commit()
        flash("User successfully created.")
    return render_template("admin_register.html")

@superadmin_login_required
def superadmin_index():
    return render_template("admin_superadmin.html")

@superadmin_login_required
def superadmin_create():
    if request.method == "POST":
        if Admin.query.filter(Admin.username == request.form["username"]).first() != None:
            flash("User already exists.", "danger")
            return redirect('/admin/superadmin/')
        nadmin = Admin(uname=request.form["username"],
                       pwhash=hashlib.sha256(request.form["password"]).hexdigest(),
                       superadmin=("superadmin" in request.form))
        db_session.add(nadmin)
        db_session.commit()
        flash("User successfully created.", "success")
        return redirect('/admin/superadmin/')
    return redirect('/admin/superadmin/')
