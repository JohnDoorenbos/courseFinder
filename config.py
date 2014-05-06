from flask import Flask, render_template, session, request
from flask_bootstrap import Bootstrap
from flask_wtf import Form
from wtforms import TextField, BooleanField, validators 
from flask.ext.sqlalchemy import SQLAlchemy

    
app = Flask(__name__)
Bootstrap(app)
app.secret_key = "luther"


app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/test.db'
db = SQLAlchemy(app)
