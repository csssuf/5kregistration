from flask import render_template, flash, session, request, redirect, Response
from project.models import RegisteredUser
from project.database import db_session
import datetime
import uuid
import smtplib
import urllib
import stripe

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

def billing(uid):

    actuser = RegisteredUser.query.filter(RegisteredUser.id == uid).first()
    if not actuser:
        flash('Invalid participant', 'danger')

    return render_template("billing.html", email=actuser.email)

def pay(uid):

    actuser = RegisteredUser.query.filter(RegisteredUser.id == uid).first()
    if not actuser:
        return Response('Invalid participant', 400)

    if request.method == "POST":
        if request.form['type'] == 'cash':
            return pay_with_cash(
                actuser,
                request.form['name'],
                request.form['price']
                )
        elif request.form['type'] == 'credit':
            return pay_with_stripe(
                actuser,
                request.form['name'],
                request.form['price'],
                request.form['token']
                )
        else:
            return Response('Invalid payment type', 400)
    else:
        return Response('Invalid payment method', 400)

def pay_with_stripe(actuser, name, req_price, stripe_token):
    stripe.api_key = "sk_test_key"

    if datetime.datetime.now() > datetime.datetime(2014, 10, 5):
        price = 1500
    else:
        price = 1000

    metadata = {
        "uid": actuser.id,
        "name": actuser.name,
    }

    if price != int(req_price):
        return Response('Incorrect price requested. Expected %d, got %d' %(price, int(req_price)), 400)
    else:
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
            return Response("Sorry, an error ocurred. Please try again in a bit.", 500)

        if charge.paid:
            actuser.name = name
            actuser.paid = True
            try:
                db_session.commit()
            except:
                return Response('Paid, but encountered an error. Please contact 5k@csh.rit.edu.', 500)

            return Response('Registered and paid', 200)
        else:
            return Response('Payment failed', 400)

def pay_with_cash(actuser, name, price):

    actuser.name = name
    try:
        db_session.commit()
    except:
        return Response('Sorry, we encountered an error. Please contact 5k@csh.rit.edu or try again later.', 500)

    return Response('Registered, but not paid (cash chosen)', 200)
