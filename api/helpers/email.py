import os
from flask import render_template, current_app
from flask_mail import Message
from api.config.initialization import mail
from api.modules.user.model import UserModel
# from threading import Thread


def send_async_email(app, msg):
    with app.app_context():
        mail.send(msg)


def __send_email(subject, recipients, html_body):
    sender = env = os.environ.get('ADMINS')[0]
    msg = Message(subject, sender=sender, recipients=recipients)
    # msg.body = text_body
    msg.html = html_body
    mail.send(msg)
    # app = current_app._get_current_object()  # get the real app instance
    # Thread(target=send_async_email, args=(app, msg)).start()


def send_password_reset_request_email(user: UserModel):
    from api.modules.user.business import get_reset_password_token
    token = get_reset_password_token(user)

    template = render_template('emailers/reset_password.html',
                               user=user, token=token)

    __send_email('Reset Your Password',
                 recipients=[user.email],
                 html_body=template)


def send_password_reset_confirmation_email(user: UserModel):
    __send_email('Your Password has been updated',
                 recipients=[user.email],
                 html_body=render_template('emailers/reset_password_request.html'))
