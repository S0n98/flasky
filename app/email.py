from flask_mail import Message
from app import mail
from flask import render_template
from app import app
from threading import Thread
from flask_babel import _

#send email in a background thread and not make this app slow down
def send_async_email(app, msg):
    with app.app_context():
        mail.send(msg)

def send_email(subject, sender, recipients, text_body, html_body):
    msg = Message(subject, sender=sender, recipients=recipients)
    msg.body = text_body
    msg.html = html_body
    Thread(args=(app, msg), target=send_async_email).start()

def  send_password_reset_email(user):
    token = user.get_reset_password_token()
    send_email('[My flask] Reset Your Password',
                sender=app.config['ADMINS'][0],
                recipients=[user.email],
                text_body=render_template('email/reset_password_mail.txt',
                                            user=user, token=token),
                html_body=render_template('email/reset_password_mail.html',
                                            user=user, token=token))
