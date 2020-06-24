from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

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

# from flask_sqlalchemy import SQLAlchemy
# from flask import Flask
#
# import os
# SECRET_KEY = os.urandom(32)
# # Grabs the folder where the script runs.
# basedir = os.path.abspath(os.path.dirname(__file__))
#
# # Enable debug mode.
# DEBUG = True
#
# # Connect to the database
# app = Flask('app')
# db = SQLAlchemy(app)
#
# # TODO IMPLEMENT DATABASE URL
# # SQLALCHEMY_DATABASE_URI = 'postgres://postgres:Ropac123@localhost:5432/fyyurapp'
# SQLALCHEMY_DATABASE_URI = 'postgres://{}:{}@{}/{}'.format('postgres', 'Ropac123', 'localhost:5432', 'capstone_db')