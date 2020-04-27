import os
from flask import render_template, current_app, url_for
from flask_mail import Message
from api.config.initialization import mail
from api.modules.user.business import generate_confirmation_token
from api.modules.user.model import UserModel


# from threading import Thread


def _send_async_email(app, msg):
    with app.app_context():
        mail.send(msg)


def __send_email(subject, recipients, html_body):
    sender = env = os.environ.get('ADMINS')[0]
    msg = Message(subject, sender=sender, recipients=recipients)
    # msg.body = text_body
    msg.html = html_body
    mail.send(msg)
    # app = current_app._get_current_object()  # get the real app instance
    # Thread(target=_send_async_email, args=(app, msg)).start()


def send_password_reset_request_email(user: UserModel) -> None:
    token = generate_confirmation_token(user.email)
    reset_url = url_for('app.user_reset_password', token=token, _external=True)

    template = render_template('emailers/reset.html',
                               user=user, reset_url=reset_url)

    __send_email('Reset Your Password',
                 recipients=[user.email],
                 html_body=template)


def send_password_reset_confirmation_email(user: UserModel) -> None:
    __send_email('Your Nasih password has changed',
                 recipients=[user.email],
                 html_body=render_template('emailers/reset_confirmed.html', user=user))


def send_email_signup(user: UserModel):
    __send_email('Welcome to Muslim Friendly Travel',
                 recipients=[user.email],
                 html_body=render_template('emailers/reset_password_request.html'))


def send_email_booking_confirmed(booking, user: UserModel):
    __send_email('Congrats! your hotel has been booked',
                 recipients=[user.email],
                 html_body=render_template('emailers/reset_password_request.html'))
