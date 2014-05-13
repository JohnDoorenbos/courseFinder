from config import *
from dbSearch import *

session = loadSession()

class CourseQueryForm(Form):
    dept = TextField('Department')
    number = TextField('Course Number')
    title = TextField('Course Title')
    gen_eds = SelectMultipleField('Gen Ed Fulfillments',
                                  choices=[('bl','BL'),
                                           ('hb','HB'),
                                           ('hbssm','HBSSM'),
                                           ('he','HE'),
                                           ('hept','HEPT'),
                                           ('hist','Hist'),
                                           ('intcl','Intcl'),
                                           ('nwl','NWL'),
                                           ('nwnl','NWNL'),
                                           ('quant','Quant'),
                                           ('rel','Rel'),
                                           ('skl','Skl'),
                                           ('wel','Wel')])

@app.route('/coursefinder', methods=['POST','GET'])
def main_page():
    print request.method
    course_query_form = CourseQueryForm(csrf_enabled=False)
    print course_query_form.validate()
    return render_template('form.html', form=course_query_form)

@app.route('/coursefinder/results')
def results_page(methods=['POST','GET']):
    course_query_form = CourseQueryForm(request.args, csrf_enabled=False)
    return render_template('results.html')

@app.route('/coursefinder/catalog')
def catalog():
    #This should have a template that will go through all of the courses and list them (much like the search)
    return "Contains all courses in the database"

@app.route('/coursefinder/catalog/<dept>/<number>')
def course_page(dept,number):
    try:
        course_id = str(dept + ' ' + number)
        res = session.query(CourseDB)
        result = search(id = course_id, ses = res)[0]
        print(result)
        return render_template("course.html",result = result)
    except:
        return 'Course does not exist'

@app.route('/coursefinder/api')
def api(methods=['POST','GET']):
    data = {'hello':'world'}
    #api will go here
    return jsonify(**data)

if __name__ == "__main__":
    app.run(debug=True)

