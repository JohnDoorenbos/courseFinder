from flask import Flask, render_template, session, request, redirect, jsonify
from flask_bootstrap import Bootstrap
from flask_wtf import Form
from wtforms import TextField, BooleanField, SubmitField, SelectMultipleField, validators 
from flask.ext.sqlalchemy import SQLAlchemy

    
app = Flask(__name__)
Bootstrap(app)
app.secret_key = "luther"
db = SQLAlchemy(app)

dbPath = 'sqlite:////tmp/CF1.db'
app.config['SQLALCHEMY_DATABASE_URI'] = dbPath






