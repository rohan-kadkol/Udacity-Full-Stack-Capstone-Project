from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os

SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL')
if not SQLALCHEMY_DATABASE_URI:
    # TODO: Modify it to match your database
    SQLALCHEMY_DATABASE_URI = 'postgres://{}:{}@{}/{}'.format(
        'postgres', 'password', 'localhost:5432', 'capstone_db')


def setup_db(app, database_path=SQLALCHEMY_DATABASE_URI):
    app.config['SQLALCHEMY_DATABASE_URI'] = database_path
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db = SQLAlchemy(app)
    return db


app = Flask('app')
db = setup_db(app)
