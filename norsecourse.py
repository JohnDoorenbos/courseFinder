from config import *

from flask import render_template, request, redirect, jsonify, flash
from dbmodels import Course, AltDesc
from dbsearch import *

from dbmisc import get_depts, next_alt_desc_id
from stringhelp import listify, id_to_url, id_from_url

from forms import CourseQueryForm, AltDescForm

dbsession = loadSession()

@app.route('/coursefinder')
def main_page():
    print request.method
    form = CourseQueryForm()
    return render_template('form.html', form=form, history=history)

@app.route("/coursefinder/results")
def results_page(methods=['POST','GET']):
    course_query_form = CourseQueryForm()
    args = preprocess_args(request.args)
    results = search(dbsession,**args)
    if len(results):
        return render_template("results.html",
                               courses = results,
                               history = history)
    else:
        return render_template("no_results.html",
                               history = history)

@app.route('/catalog')
def catalog():
    dept_list = sorted(get_depts(dbsession))
    return render_template('catalog.html',depts=dept_list, history=history)

@app.route('/catalog/<dept>')
def dept_page(dept):
    dept = dept.upper()

    res = dbsession.query(CourseDB)
    course_list = list(res.filter(CourseDB.dept == dept))
    course_list.sort(key = lambda c: c.id)

    return render_template('dept.html',dept=dept,courses=course_list,history=history)

@app.route('/catalog/<dept>/<course_id>')
def course_page(dept, course_id):
    try: #format id, else tell user that id is invalid
        formatted_id = id_from_url(course_id)
    except ValueError:
        return '\''+course_id+'\' is not a valid course id.'

    try:
        res = dbsession.query(CourseDB)
        result = res.filter(CourseDB.id == formatted_id).one()
    except:
        return 'Course \'' + course_id + '\' does not exist.'

    #get alt descs for course
    res = dbsession.query(AltDescDB)
    alt_desc_list = list(res.filter(AltDescDB.course_id == formatted_id))

    #get alt descs for courses that are the same (like CS220 and MATH220)
    #and concatenate them together
    res = dbsession.query(CourseDB)
    course = res.filter(CourseDB.id == formatted_id).one()
    for same_course in listify(course.same_as):
        additional_alt_descs = dbsession.query(AltDescDB).filter(AltDescDB.course_id == same_course)
        alt_desc_list += list(additional_alt_descs)

    form = AltDescForm()
        
    #Appends course title to history
    history.add(result)

    return render_template("course.html", course=result, form=form, history = history, alt_descs=alt_desc_list)

@app.route('/catalog/<dept>/<course_id>/submit')
def submit_alt_desc(dept, course_id, methods=['POST','GET']):
    formatted_id = id_from_url(course_id)
    form = AltDescForm(request.args)
    if form.validate():
        print 'form validated'
        alt_desc = AltDesc(next_alt_desc_id(dbsession),form.content.data,str(formatted_id))
        db.session.add(alt_desc)
        db.session.commit()
        flash('Thanks for submitting an alternative description')
    return redirect('/catalog/'+dept+"/"+course_id)

@app.route('/about')
def about_page():
    return render_template('about.html', history = history)

@app.route('/api')
def api(methods=['POST','GET']):
    args = preprocess_args(request.args)
    data = search(dbsession,**args)
    return jsonify(**data)

@app.route('/api/docs')
def api_docs():
    return render_template('api_docs.html', history = history)

@app.route('/')
def go_to_main_page():
    return redirect('/coursefinder')

if __name__ == "__main__":
    app.run(debug=True)
