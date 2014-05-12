from config import *
from dbSearch import *

session = loadSession()

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

@app.route('/courseFinder/catalog')
def catalog():
    #This should have a template that will go through all of the courses and list them (much like the search)
    return "Contains all courses in the database"

@app.route('/courseFinder/<dept>/<number>')
def course_page(dept,number):
    course_id = str(dept + ' ' + number)
    res = session.query(CourseDB)
    result = search(id = course_id, ses = res)[0]
    print(result)
    return render_template("course.html",result = result)
    
if __name__ == "__main__":
    app.run(debug=True)

