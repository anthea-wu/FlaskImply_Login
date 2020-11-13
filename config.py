import os, datetime
from datetime import timedelta

class Config:
    path = os.path.abspath(os.path.dirname(__file__))
    DEBUG = True
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(path, 'member/static/data/register.sqlite')
    SECRET_KEY = os.environ.get('SECRET_KEY')


    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')


    REMEMBER_COOKIE_DURATION = timedelta(minutes=10)
    # https://stackoverflow.com/questions/13831251/flask-login-chrome-ignoring-cookie-expiration
    # How long to remember logged in user even if he closed the browser.

    PERMANENT_SESSION_LIFETIME = timedelta(minutes=10)
    # https://stackoverflow.com/questions/13831251/flask-login-chrome-ignoring-cookie-expiration
    # To force login session to expire after some time (even if the browser is still kept running)
    