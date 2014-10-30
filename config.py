from flask import Flask, render_template, session, request, redirect, jsonify, flash
from flask_bootstrap import Bootstrap
from flask_wtf import Form
from wtforms import IntegerField, TextAreaField, TextField, BooleanField, SubmitField, SelectMultipleField, validators 
from flask.ext.sqlalchemy import SQLAlchemy

import os
#import psycopg2
#import urlparse

    
app = Flask(__name__)
Bootstrap(app)
app.secret_key = "luther"

db = SQLAlchemy(app)

if 'DATABASE_URL' in os.environ:
    dbPath =  'postgresql+pg8000://flnqsqilzhheoo:mkz5h36UA7R63Om9dPPQ1X4M5i@ec2-54-83-196-217.compute-1.amazonaws.com:5432/dcagbs1vl8cb22'#os.environ['DATABASE_URL']
else:
    dbPath = 'sqlite:////tmp/cf.db'


app.config['SQLALCHEMY_DATABASE_URI'] =  dbPath


class History(): #Doesn't update when back button is used. 
    '''This Class stores the ten last course pages visited by the user. Note: it stores the database course entry. It has an add function that takes a course, and enters it into the course list so long as the course isn't already in the list. The history class has a maxLength of 10 (currently)'''
 
    def __init__(self):
        self.courses = []
        self.maxLength = 10
    def add(self, course):
        if course not in self.courses:
            self.courses.insert(0,course)
        else:
            self.courses.remove(course)
            self.courses.insert(0,course)
        if len(self.courses) > self.maxLength:
            self.courses.pop() 
    def __str__(self):
        result = ''
        for course in self.courses:
            result += course.title + ", "
            
        return(result)

history = History()            
'''           
urlparse.uses_netloc.append("postgres")
url = urlparse.urlparse(os.environ['DATABASE_URL'])

conn = psycopg2.connect(
    database = url.path[1:],
    user = url.username,
    password=url.password,
    host=url.hostname,
    port=url.port
)
    
'''
