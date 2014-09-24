from flask import render_template, flash, session, request, redirect
from project.models import RegisteredUser
from project.database import db_session
import datetime
import uuid

def reg():
    if request.method == "POST":
        if RegisteredUser.query.filter(RegisteredUser.email ==
                request.form["email"]).first() != None:
            flash("Error: that email is already registered.")
            return redirect('/')
        reguuid = uuid.uuid1()
        newuser = RegisteredUser(email=request.form["email"],
                date=datetime.datetime.now(), reg_uuid = reguuid)
        db_session.add(newuser)
        db_session.commit()
        flash("Successfully registered.")
        return redirect('/')

def verify():
    if not request.args or not "key" in request.args or not "user" in request.args:
        return redirect('/')
    actuser = RegisteredUser.query.filter(RegisteredUser.email == request.args["user"]).first()
    if not actuser:
        return redirect('/')
    if actuser.paid:
        return redirect('/')
    if actuser.reg_uuid == request.args["key"]:
        actuser.emailverified = True
        db_session.commit()
        return redirect('/payment/')
    return render_template("verify.html")

def billing():
    return render_template("billing.html")
