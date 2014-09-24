from flask import render_template, flash, session, request, redirect
from project.models import RegisteredUser
from project.database import db_session
import datetime
import uuid
import smtplib
import urllib

def reg():
    if request.method == "POST":
        if RegisteredUser.query.filter(RegisteredUser.email ==
                request.form["email"]).first() != None:
            flash("Error: that email is already registered.")
            return redirect('/')
        reguuid = uuid.uuid1()
        mail = """From: 5k@csh.rit.edu\r\nTo: %s\r\nSubject: CSH 5K Email Confirmation\r\n\r\nWelcome to the CSH 5K for Charity: Water!

To confirm your email address, please click here: http://5k.csh.rit.edu/verify?key=%s&user=%s""" % (request.form["email"], reguuid, urllib.quote(request.form["email"]))
        server = smtplib.SMTP("mail.csh.rit.edu")
        server.sendmail("5k@csh.rit.edu", [request.form["email"]], mail)
        server.quit()
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
