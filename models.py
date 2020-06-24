from datetime import datetime

from config import db
# from app import db
from flask_sqlalchemy import SQLAlchemy

# db = SQLAlchemy()
# SQLALCHEMY_DATABASE_URI = 'postgres://{}:{}@{}/{}'.format('postgres',
#                                                           'Ropac123',
#                                                           'localhost:5432',
#                                                           'capstone_db')
#
# def setup_db(app, database_path=SQLALCHEMY_DATABASE_URI):
#     print('1-')
#     app.config['SQLALCHEMY_DATABASE_URI'] = database_path
#     print('2-')
#     app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
#     print('3-')
#     db.app = app
#     print('4-')
#     db.init_app(app)
#     print('5-')
#     db.create_all()
#     return db


# project_volunteer = db.Table('project_volunteer',
#                        db.Column('project_id', db.Integer, db.ForeignKey('projects.id'), primary_key=True),
#                        db.Column('volunteer_id', db.Integer, db.ForeignKey('volunteers.id'), primary_key=True))

class Project(db.Model):
    __tablename__ = 'projects'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(), nullable=False)
    description = db.Column(db.String(), nullable=False)
    email = db.Column(db.String(), nullable=False)
    phone = db.Column(db.String())
    # volunteers = db.relationship('Volunteer', secondary=project_volunteer, backref=db.backref('projects'))

    def __repr__(self):
        return f'______\n' \
               f'id: {self.id}\n' \
               f'name: {self.name}\n' \
               f'description: {self.description}\n' \
               f'email: {self.email}\n' \
               f'phone: {self.phone}\n' \
               f'______\n\n'

    def format(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'email': self.email,
            'phone': self.phone
        }


class Volunteer(db.Model):
    __tablename__ = 'volunteers'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(), nullable=False)
    email = db.Column(db.String(), nullable=False)
    phone = db.Column(db.String())

    def __repr__(self):
        return f'______\n' \
               f'id: {self.id}\n' \
               f'name: {self.name}\n' \
               f'email: {self.email}\n' \
               f'phone: {self.phone}\n' \
               f'______\n\n'

    def format(self):
        return {
            'id': self.id,
            'name': self.name,
            'email': self.email,
            'phone': self.phone
        }
