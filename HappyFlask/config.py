import os

class Config:
    root = os.path.abspath(os.path.dirname(__file__))
    DEBUG = True
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' +  os.path.join(root, 'static\\data\\data_register.sqlite')
    SECRET_KEY = 'your key'