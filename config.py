from flask import Flask
from flask_bootstrap import Bootstrap
from flask.ext.sqlalchemy import SQLAlchemy

import os
    
app = Flask(__name__)
Bootstrap(app)
app.secret_key = "luther" #needed for flask WTForms, since it uses csrf (even though we then disable it)

db = SQLAlchemy(app)

if 'DATABASE_URL' in os.environ: #use postgres if on Heroku
    dbPath =  'postgresql+pg8000://flnqsqilzhheoo:mkz5h36UA7R63Om9dPPQ1X4M5i@ec2-54-83-196-217.compute-1.amazonaws.com:5432/dcagbs1vl8cb22'
else: #or use sqlite locally
    dbPath = 'sqlite:////tmp/cf.db'


app.config['SQLALCHEMY_DATABASE_URI'] =  dbPath
