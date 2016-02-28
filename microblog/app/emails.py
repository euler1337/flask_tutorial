from flask.ext.mail import Message
from app import mail
from flask import render_template
from config import ADMINS

from threading import Thread
from app import app
from .decorators import async

# Send mail in different thread in order to not lock up the main thread in sending emails.
@async
def send_asynch_email(app, msg):
	with app.app_context():
		mail.send(msg)

def send_email(subject, sender, recipients, text_body, html_body):
	msg = Message(subject, sender=sender, recipients=recipients)
	msg.body= text_body
	msg.html = html_body
	send_asynch_email(app, msg)

def follower_notification(followed, follower):
    send_email("[microblog] %s is now following you!" % follower.nickname,
               ADMINS[0],
               [followed.email],
               render_template("follower_email.txt", 
                               user=followed, follower=follower),
               render_template("follower_email.html", 
                               user=followed, follower=follower))

    send_email("[microblog] you are now following %s!" % followed.nickname,
               ADMINS[0],
               [follower.email],
               render_template("followed_email.txt", 
                               user=follower, followed=followed),
               render_template("followed_email.html", 
                               user=follower, followed=followed))