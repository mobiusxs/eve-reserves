from os import environ

SECRET_KEY = environ['SECRET_KEY']
SQLALCHEMY_DATABASE_URI = environ['DATABASE_URL']
SQLALCHEMY_TRACK_MODIFICATIONS = False
