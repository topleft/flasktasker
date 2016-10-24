import os

basedir = os.path.abspath(os.path.dirname(__file__))

DATABASE = 'flasktaskr.db'
WTF_CSRF_ENABLED = True
SECRET_KEY = 'myprecious'
SQLALCHEMY_TRACK_MODIFICATIONS = False
DATABASE_PATH = os.path.join(basedir, DATABASE)
DEBUG = False
SQLALCHEMY_DATABASE_URI = 'sqlite:///' + DATABASE_PATH
