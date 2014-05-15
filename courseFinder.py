from config import *
from dbSearch import *
import re, random

dbsession = loadSession()

class CustomForm(Form):
    def remove_csrf(self):
        self.__delitem__('csrf_token')
        self.csrf_enabled = False
        return self

class CourseQueryForm(CustomForm):
    dept = TextField('Department', id="dept")
    #number = TextField('Course Number',[validators.Length(min=3, max=4)], id="number")
    title = TextField('Course Title', id="title")
    gen_eds = SelectMultipleField('Gen Ed Fulfillments',
                                  choices=[('',''),
                                           ('bl','BL'),
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
                                           ('wel','Wel')], id="gen_eds")

class ReviewForm(CustomForm):
    stars = IntegerField('Stars (1-5)', [validators.DataRequired(),
                                         validators.NumberRange(1,5)])
    content = TextAreaField('Content')

@app.route('/coursefinder')
def main_page():
    print request.method
    form = CourseQueryForm().remove_csrf()
    return render_template('form.html', form=form)

@app.route("/coursefinder/results")
def results_page(methods=['POST','GET']):
    course_query_form = CourseQueryForm().remove_csrf()
    res = dbsession.query(CourseDB)
    gen_eds_list = request.args.getlist("gen_eds")
    search_string = "search("
    for i in request.args:
        if i != "gen_eds":
            search_string += i+"="+"'"+request.args[i]+"'"+", "

    new_search_string = ""
    to_become_set = []
    if len(gen_eds_list) == 0:
        search_string += "ses = res)"
        to_become_set = eval(search_string)
    for gen_ed in gen_eds_list:
        new_search_string = search_string+"gen_eds = "+"'"+gen_ed+"'" + ", ses = res)"
        temp = eval(new_search_string)
        print(new_search_string)
        print(temp)
        to_become_set += temp
    
    result = set(to_become_set)
    print("")
    print(result)
    
    
    
    #lst = eval(search_string)
    #print(lst)
    return render_template("results.html", lst = result)

@app.route('/coursefinder/catalog')
def catalog():
    #This should have a template that will go through all of the courses and list them (much like the search)
    return "Contains all courses in the database"


@app.route('/coursefinder/catalog/<course_id>')
def course_page(course_id):
    try:
        formatted_id = course_id.upper()
        match = re.match('^([A-Z]+)(\d{3}.?)$',formatted_id)
        if match:
            formatted_id = str(match.group(1) + ' ' + match.group(2))
        else:
            return '\'' + course_id + '\' is not a valid course id.'
        res = dbsession.query(CourseDB)
        result = search(id = formatted_id, ses = res)[0]
        form = ReviewForm().remove_csrf()
        return render_template("course.html", result=result, form=form, course_id=course_id)
    except IndexError:
        return 'Course does not exist.'

def next_review_id():
    return random.randrange(10000)

@app.route('/coursefinder/catalog/<course_id>/submit')
def submit_review(course_id, methods=['POST','GET']):
    formatted_id = course_id.upper()
    match = re.match('^([A-Z]+)(\d{3}.?)$',formatted_id)
    if match:
        formatted_id = str(match.group(1) + ' ' +
                                  match.group(2))
    form = ReviewForm(request.args).remove_csrf()
    if form.validate():
        print 'form validated'
        review = Review(next_review_id(),form.stars.data,form.content.data,str(formatted_id))
        db.session.add(review)
        db.session.commit()
        flash('Thanks for submitting a review')
    return redirect('/coursefinder/catalog/'+course_id)
    return 'Hello, '+course_id+'!'

@app.route('/coursefinder/api')
def api(methods=['POST','GET']):
    data = {'hello':'world'}
    #api will go here
    return jsonify(**data)

if __name__ == "__main__":
    app.run(debug=True)

