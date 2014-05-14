from flask import Flask, render_template, session, request, redirect, jsonify
from flask_bootstrap import Bootstrap
from flask_wtf import Form
from wtforms import IntegerField, TextAreaField, TextField, BooleanField, SubmitField, SelectMultipleField, validators 
from flask.ext.sqlalchemy import SQLAlchemy



    
app = Flask(__name__)
Bootstrap(app)
app.secret_key = "luther"

db = SQLAlchemy(app)
dbPath = 'sqlite:////tmp/CF1.db'
app.config['SQLALCHEMY_DATABASE_URI'] = dbPath

#------------------Defining our Models for the database----------------------------------------------

course_offerings = db.Table('course_offerings',
                            db.Column('course_id',db.Text, db.ForeignKey('courses.id')),
                            db.Column('prof_name',db.Text, db.ForeignKey('professors.name'))
)


class Course(db.Model):
    __tablename__ = "courses"
    title = db.Column(db.Text)
    dept = db.Column(db.Text)
    number = db.Column(db.Text)
    desc  = db.Column(db.Text)
    hours = db.Column(db.Text)
    gen_eds = db.Column(db.Text)
    prereqs = db.Column(db.Text)
    id = db.Column(db.Text, primary_key = True)
    professors = db.relationship("Professor",secondary = course_offerings)
    same_as = db.Column(db.Text)
    def __init__(self, title, dept, number, desc, gen_eds, prereqs, id, professors, hours, same_as):
        self.title = title
        self.dept = dept
        self.number = number
        self.desc = desc
        self.hours = hours
        self.gen_eds = gen_eds
        self.prereqs = prereqs
        self.id = id
        self.professors = professors
        self.same_as = same_as

class Review(db.Model):
    __tablename__ = "reviews"
    review_id = db.Column(db.Integer, primary_key = True)
    stars = db.Column(db.Integer)
    content = db.Column(db.Text)
    course_id = db.Column(db.Text, db.ForeignKey('courses.id'))

    def __init__(self, review_id, stars, content, course_id):
        self.review_id = review_id
        self.stars = stars
        self.content = content
        self.course_id

class Professor(db.Model):
    __tablename__ = "professors"
    name =  db.Column(db.Text, primary_key = True)
    bio =  db.Column(db.Text)
    department =  db.Column(db.Text)
    courses = db.relationship("Course", secondary = course_offerings)
    
    def __init__(self,name, bio, department, courses):
        self.name = name
        self.bio = bio
        self.department = department
        self.courses = courses
