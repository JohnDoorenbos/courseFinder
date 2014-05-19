from config import *
from dbSearch import *
from forms import CourseQueryForm, ReviewForm
import re, random

dbsession = loadSession()

def listify(s):
    if s == 'N/A':
        return []
    else:
        return [i.strip() for i in s.split(',')]

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

def get_depts():
    res = dbsession.query(CourseDB)

    dept_list = []
    for course in res:
        if course.dept not in dept_list:
            dept_list.append(course.dept)

    return dept_list

def get_review_ids():
    res = dbsession.query(ReviewDB)
    review_id_list = [review.review_id for review in res]
    return review_id_list

def next_review_id():
    review_id_list = sorted(get_review_ids())
    if 0 not in review_id_list:
        return 0
    else:
        for review_id in review_id_list:
            new_id = review_id + 1
            if new_id not in review_id_list:
                return new_id

@app.route('/coursefinder')
def main_page():
    print request.method
    form = CourseQueryForm().remove_csrf()
    return render_template('form.html', form=form, history=history)

@app.route("/coursefinder/results")
def results_page(methods=['POST','GET']):
    course_query_form = CourseQueryForm().remove_csrf()
    result = results_page_search(dbsession,request)
    
    return render_template("results.html", courses = sorted(list(result), key = lambda c: c.id), history = history)

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

@app.route('/coursefinder/catalog/<dept>/<course_id>')
def course_page(dept, course_id):
    try: #format id, else tell user that id is invalid
        formatted_id = format_id(course_id)
    except ValueError:
        return '\''+course_id+'\' is not a valid course id.'

    try:
        res = dbsession.query(CourseDB)
        result = res.filter(CourseDB.id == formatted_id).one()
    except:
        return 'Course \'' + course_id + '\' does not exist.'

    #get reviews for course
    res = dbsession.query(ReviewDB)
    review_list = list(res.filter(ReviewDB.course_id == formatted_id))

    #get reviews for courses that are the same (like CS220 and MATH220)
    #and concatenate them together
    res = dbsession.query(CourseDB)
    course = res.filter(CourseDB.id == formatted_id).one()
    for same_course in listify(course.same_as):
        additional_reviews = dbsession.query(ReviewDB).filter(ReviewDB.course_id == same_course)
        review_list += list(additional_reviews)

    form = ReviewForm().remove_csrf()
        
    #Appends course title to history
    history.add(result)

    return render_template("course.html", course=result, form=form, history = history, reviews=review_list)

@app.route('/coursefinder/catalog/<dept>/<course_id>/submit')
def submit_review(dept, course_id, methods=['POST','GET']):
    formatted_id = format_id(course_id)
    form = ReviewForm(request.args).remove_csrf()
    if form.validate():
        print 'form validated'
        review = Review(next_review_id(),form.stars.data,form.content.data,str(formatted_id))
        db.session.add(review)
        db.session.commit()
        flash('Thanks for submitting a review')
    return redirect('/coursefinder/catalog/'+dept+"/"+course_id)
    
@app.route('/coursefinder/api')
def api(methods=['POST','GET']):
    data = {'hello':'world'}
    #api will go here
    return jsonify(**data)

@app.route('/')
def go_to_main_page():
    return redirect('/coursefinder')

if __name__ == "__main__":
    app.run(debug=True)
