from config import *
from dbSearch import *
from forms import CourseQueryForm, ReviewForm
import re, random

dbsession = loadSession()

def format_id(course_id):
    #takes an id like 'cs200' and return 'CS 200'
    #mostly used for preparing ids from urls to be used in the database
    formatted_id = course_id.upper()
    match = re.match('^([A-Z]+)(\d{3}.?)$',formatted_id)
    if match:
        formatted_id = str(match.group(1) + ' ' + match.group(2))
        return formatted_id
    else:
        raise(ValueError,'\''+course_id+'\' is not a valid course id')

def next_review_id():
    res = dbsession.query(ReviewDB)
    review_id_list = res.filter(ReviewDB.review_id).all()
    #print(review_id_list)
    #print(res)
    return random.randrange(10000)

def get_depts():
    res = dbsession.query(CourseDB)

    dept_list = []
    for course in res:
        if course.dept not in dept_list:
            dept_list.append(course.dept)

    return dept_list

@app.route('/coursefinder')
def main_page():
    print request.method
    form = CourseQueryForm().remove_csrf()
    return render_template('form.html', form=form, history=history)

@app.route("/coursefinder/results")
def results_page(methods=['POST','GET']):
    course_query_form = CourseQueryForm().remove_csrf()
    result = results_page_search(dbsession,request)
    
    #appears to be a bug with the sorted(list(result) clause. 
    #When searching for the hist gen_ed, one often gets the courses in different orders.
    return render_template("results.html", lst = sorted(list(result)), history = history)

@app.route('/coursefinder/catalog')
def catalog():
    dept_list = sorted(get_depts())
    return render_template('catalog.html',depts=dept_list, history=history)

@app.route('/coursefinder/catalog/<dept>')
def dept_page(dept):
    dept = dept.upper()

    res = dbsession.query(CourseDB)
    course_list = res.filter(CourseDB.dept == dept)

    return render_template('dept.html',dept=dept,courses=course_list,history=history)

@app.route('/coursefinder/catalog/<course_id>')
def course_page(course_id):
    try: #format id, else tell user that id is invalid
        formatted_id = format_id(course_id)
    except ValueError:
        return '\''+course_id+'\' is not a valid course id.'

    try: #get course from db, else tell user course does not exist
        res = dbsession.query(CourseDB)
        result = res.filter(CourseDB.id == formatted_id).one()
        #result = search(id = formatted_id, ses = res)[0]
    except IndexError:
        return 'Course \'' + course_id + '\' does not exist.'

    #get reviews for course
    res = dbsession.query(ReviewDB)
    review_list = list(res.filter(ReviewDB.course_id == formatted_id))

    #get reviews for courses that are the same (like CS220 and MATH220)
    #and concatenates them together
    res = dbsession.query(CourseDB)
    course = res.filter(CourseDB.id == formatted_id).one()
    for same_course in eval(course.same_as):
        additional_reviews = dbsession.query(ReviewDB).filter(ReviewDB.course_id == same_course)
        review_list += list(additional_reviews)

    form = ReviewForm().remove_csrf()
        
    #Appends course title to history
    history.add(result)

    return render_template("course.html", result=result, form=form, course_id=course_id, history = history, reviews=review_list)

@app.route('/coursefinder/catalog/<course_id>/submit')
def submit_review(course_id, methods=['POST','GET']):
    formatted_id = format_id(course_id)
    form = ReviewForm(request.args).remove_csrf()
    if form.validate():
        print 'form validated'
        review = Review(next_review_id(),form.stars.data,form.content.data,str(formatted_id))
        db.session.add(review)
        db.session.commit()
        flash('Thanks for submitting a review')
    return redirect('/coursefinder/catalog/'+course_id)
    
@app.route('/coursefinder/api')
def api(methods=['POST','GET']):
    data = {'hello':'world'}
    #api will go here
    return jsonify(**data)

@app.route('/')
def go_to_main_page():
    return redirect('/coursefinder')
    

if __name__ == "__main__":
    app.run(debug=True) #, use_reloader = False)

