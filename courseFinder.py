from config import *

class My_Form(Form): #Is this good for a variable name?
    name = TextField('Name',[validators.Length(min=4, max=25)])
    department = BooleanField('Spring 2014', [validators.Required()])
    submit = SubmitField('Submit')

@app.route('/courseFinder', methods=['POST', 'GET'])
def forms_page():
    if request.method == 'GET':
        print 'Request == \'GET\''
        print 'request.args:', str([key for key in request.args.keys()])
        form = My_Form(request.args)
    else:
        print 'not Request == \'GET\''
        form = My_Form()
    print form.name.data, form.department.data
    print form.validate()
    print form.validate_on_submit()
    if form.validate_on_submit():
        
        return redirect('/success')  #success will have to be the name of our next app.route
    
    return render_template("form.html",form = form)

@app.route("/results")
def results_page():
    return render_template("results.html")

@app.route('/<dept>/<number>')
def course_page(dept,number):
    course_id = dept + ' ' + number

if __name__ == "__main__":
    app.run(debug=True)
