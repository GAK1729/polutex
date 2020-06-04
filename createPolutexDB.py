from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import csv
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
import copy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres+psycopg2://postgres:xyz@localhost:1234/xyz'



app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

db = SQLAlchemy(app)


class userDB(db.Model):
    __tablename__ = "userDB"
    Username  = db.Column(db.String, primary_key=True)
    Password = db.Column(db.String, nullable=False)
    Name = db.Column(db.String, nullable=False)
    Age  = db.Column(db.Integer, nullable=False)
    Gender  = db.Column(db.String, nullable=False)
    Nationality =  db.Column(db.String, nullable=False)
    Phone_number = db.Column(db.String, nullable=False)
    Emergency_contact_number = db.Column(db.String, nullable=False)
    Email = db.Column(db.String, nullable=False)
    Health_condition = db.Column(db.String, nullable=True)

    def add_user(Username, Password, Name, Age, Gender, Nationality, Phone_number, Emergency_contact_number, Email, Health_condition):
        b = userDB(Username=Username, Password=Password, Name=Name, Age=Age, Gender=Gender, Nationality=Nationality, Phone_number=Phone_number, Emergency_contact_number=Emergency_contact_number, Email=Email, Health_condition=Health_condition)
        db.session.add(b)
        db.session.commit()



db.create_all()
