import os
from datetime import timedelta
basedir = os.path.abspath(os.path.dirname(__file__))

ACCESS_EXPIRES = {
    'access': timedelta(minutes=1),
    'refresh': timedelta(days=1)
}

class Config(object):
    WTF_CSRF_ENABLED = False
    DEBUG = False
    DEVELOPMENT = False
    SECRET_KEY = 'secret'
    FLASK_SECRET = SECRET_KEY
    JWT_SECRET_KEY = "super-secret" 
    JWT_ACCESS_TOKEN_EXPIRES = ACCESS_EXPIRES['access']
    JWT_REFRESH_TOKEN_EXPIRES = ACCESS_EXPIRES['refresh']

class DevConfig(Config):
    DEVELOPMENT = True
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, "instance\\site.sqlite")
    SQLALCHEMY_TRACK_MODIFICATIONS = False

class TestConfig(Config):
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, "instance\\test-db.sqlite")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    WTF_CSRF_ENABLED = False
    SERVER_NAME = '127.0.0.1:5000'

class ProdConfig(Config):
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, "instance\\site.sqlite")

    
config = {
    'dev': DevConfig,
    'prod': ProdConfig,
    'default': DevConfig,
    'test': TestConfig
}