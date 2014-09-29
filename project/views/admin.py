from flask import render_template, request, session, flash, redirect
from project.utils.auth import admin_login_required, superadmin_login_required
from project.models import Admin, RegisteredUser
from project.database import db_session
import hashlib

@admin_login_required
def listusers():
    return render_template("admin_listusers.html",
            users=db_session.query(RegisteredUser).order_by(RegisteredUser.id))

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

@superadmin_login_required
def superadmin_index():
    return render_template("admin_superadmin.html")

@superadmin_login_required
def superadmin_create():
    if request.method == "POST":
        if Admin.query.filter(Admin.username == request.form["username"].first()) != None:
            flash("User already exists.", "danger")
            return redirect('/admin/superadmin/')
        nadmin = Admin(uname=request.form["username"],
                       pwhash=hashlib.sha256(request.form["password"]).hexdigest(),
                       superadmin=request.form["superadmin"])
        db_session.add(nadmin)
        db_session.commit()
        flash("User successfully created.", "success")
        return redirect('/admin/superadmin/')
    return redirect('/admin/superadmin/')
