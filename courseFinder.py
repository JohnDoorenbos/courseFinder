from flask import Flask, render_template, session, request
from flask_bootstrap import Bootstrap
from flask_wtf import Form
from wtforms import TextField, BooleanField, validators 
from flask.ext.sqlalchemy import SQLAlchemy


class My_Form(Form): #Is this good for a variable name?
    name = TextField('Name')#,[validators.Length(min=1,max=25)])
    department = BooleanField('Spring 2014')#, [validators.Required()])
    
    
app = Flask(__name__)
Bootstrap(app)
app.secret_key = "luther"


app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/test.db'
db = SQLAlchemy(app)


@app.route('/courseFinder')
def forms_page():
    form = My_Form()
    print(form.name.data, "   ", form.department.data)
    print(form.validate())
    if form.validate_on_submit():
        
        return redirect('/success')  #success will have to be the name of our next app.route
    
    return render_template("form.html",form = form)

@app.route("/results")
def results_page():
    return render_template("results.html")
if __name__ == "__main__":
    app.run(debug=True)
