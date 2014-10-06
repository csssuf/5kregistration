from flask import render_template, flash, session, request, redirect, Response
from project.models import RegisteredUser
from project.database import db_session
import datetime
import uuid
import smtplib
import urllib
import stripe
import re

def reg():
    if request.method == "POST":
        if RegisteredUser.query.filter(RegisteredUser.email ==
                request.form["email"]).first() != None:
            flash("Error: that email is already registered.", "danger")
            return redirect('/')
        reguuid = uuid.uuid1()
        mail = """From: 5k@csh.rit.edu\r\nTo: %s\r\nSubject: CSH 5K Email Confirmation\r\n\r\nWelcome to the CSH 5K for Charity: Water!

To confirm your email address, please click here: http://5k.csh.rit.edu/verify?key=%s&user=%s""" % (request.form["email"], reguuid, urllib.quote(request.form["email"]))
        try:
            server = smtplib.SMTP("mail.csh.rit.edu")
            server.sendmail("5k@csh.rit.edu", [request.form["email"]], mail)
            server.quit()
        except:
            flash("An error occurred sending you an email. Please try again or contact 5k@csh.rit.edu.", "danger")
            return redirect('/')
        newuser = RegisteredUser(email=request.form["email"],
                date=datetime.datetime.now(), reg_uuid = str(reguuid))
        db_session.add(newuser)
        db_session.commit()
        flash("Successfully registered.", "success")
        return redirect('/')

def verify():
    if not request.args or not "key" in request.args or not "user" in request.args:
        return redirect('/')
    actuser = RegisteredUser.query.filter(RegisteredUser.email == request.args["user"]).first()
    if not actuser:
        return redirect('/')
    if actuser.paid >= 1000:
        flash("You have already paid.", "success")
        return redirect('/')
    if actuser.reg_uuid == request.args["key"]:
        actuser.emailverified = True
        db_session.commit()
        return redirect('/billing/%d/' % actuser.id)
    return render_template("verify.html")

def billing(uid):
    actuser = get_current_user(uid)
    if not actuser:
        return redirect('/')
    elif not actuser.emailverified:
        flash("Please verify your email.", "danger")
        return redirect('/verify/')
    elif actuser.paid >= 0:
        flash("You have already paid.", "success")
        return redirect('/')
    return render_template("billing.html", email=actuser.email)

def pay(uid):
    actuser = get_current_user(uid)
    if not actuser:
        return redirect('/')
    elif not actuser.emailverified:
        flash("Please verify your email.", "danger")
        return redirect('/verify/')
    elif actuser.paid >= 0:
        flash("You have already paid.", "success")
        return redirect('/')
    if request.method == "POST":
        errors = ""

        if len(request.form['name']) < 1 or re.search(".{2,}\s+.+", request.form['name']) == None:
            errors += "Please provide your full name.<br>"

        if len(request.form['phone']) < 1:
            errors += "Please provide your phone number.<br>"

        if request.form['racetype'] != '5k' and request.form['racetype'] != 'funrun':
            errors += "Please select the type of race.<br>"

        if datetime.datetime.now() >= datetime.datetime(2014, 10, 18):
            min_price = 1500
        else:
            min_price = 1000

        if int(request.form['price']) < min_price:
            errors += 'A minimum donation of $%d is required.<br>' %(min_price / 100)

        if len(errors) > 0:
            return Response(errors, 400)

        if request.form['type'] == 'cash':
            return pay_with_cash(
                actuser,
                request.form['name'],
                request.form['phone'],
                request.form['racetype'],
                request.form['price']
                )
        elif request.form['type'] == 'credit':
            return pay_with_stripe(
                actuser,
                request.form['name'],
                request.form['phone'],
                request.form['racetype'],
                request.form['price'],
                request.form['token']
                )
        else:
            return Response('Invalid payment type', 400)
    else:
        return Response('Invalid payment method', 400)

def pay_with_stripe(actuser, name, phone, racetype, price, stripe_token):
    stripe.api_key = "sk_test_key"

    actuser.name     = name
    actuser.phone    = ''.join(c for c in phone if c.isdigit())
    actuser.racetype = racetype

    metadata = {
        "uid": actuser.id,
        "name": actuser.name,
        "phone": actuser.phone,
        "racetype": actuser.racetype,
    }

    try:
        charge = stripe.Charge.create(
          amount=price,
          currency="usd",
          card=stripe_token,
          description="Registration fee for CSH Costume 5K",
          receipt_email=actuser.email,
          metadata=metadata
        )
    except stripe.CardError as e:
        return Response(e.message + " Please try again.", 400)
    except (stripe.InvalidRequestError, stripe.AuthenticationError, stripe.APIConnectionError, stripe.StripeError) as e:
        return Response("Sorry, an error ocurred. Your card was not charged. Please try again in a bit or contact 5k@csh.rit.edu.", 500)

    if charge.paid:
        actuser.paid = charge.amount
        try:
            db_session.commit()
        except:
            return Response('Paid, but encountered an error. Please contact 5k@csh.rit.edu.', 500)

        return Response('Registered and paid', 200)
    else:
        return Response('Payment failed', 400)

def pay_with_cash(actuser, name, phone, racetype, price):
    actuser.name     = name
    actuser.phone    = ''.join(c for c in phone if c.isdigit())
    actuser.racetype = racetype
    actuser.paid     = 0
    try:
        db_session.commit()
    except:
        return Response('Sorry, we encountered an error. Please contact 5k@csh.rit.edu or try again later.', 500)

    return Response('Registered, but not paid (cash chosen)', 200)

def get_current_user(uid):
    debug = False
    if debug:
        actuser       = RegisteredUser()
        actuser.id    = uid
        actuser.email = "test@example.com"
        actuser.emailverified = True
    else:
        actuser = RegisteredUser.query.filter(RegisteredUser.id == uid).first()
        if not actuser:
            flash('Invalid participant', 'danger')
    return actuser
