import os

class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'averysecretkey'
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:root@localhost:3306/survey_db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
