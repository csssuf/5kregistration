from flask import render_template, flash, session, request, redirect
from project.models import RegisteredUser
from project.database import db_session


def reg():
    if request.method == "POST":
        if RegisteredUser.query.filter(RegisteredUser.email ==
                request.form["email"]).first() != None:
            flash("Error: that email is already registered.")
            return redirect('/')
        newuser = RegisteredUser(email=request.form["email"])
        db_session.add(newuser)
        db_session.commit()
        flash("Successfully registered.")
        return redirect('/')
