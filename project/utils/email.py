import smtplib

def send_email(recipient, message):
    try:
        server = smtplib.SMTP("mail.csh.rit.edu")
        server.sendmail("5k@csh.rit.edu", recipient, message)
        server.quit()
    except i:
	print i
        return False
    return True
