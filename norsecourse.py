from config import *

from flask import request, redirect, jsonify, flash, make_response
from flask import render_template as flask_render_template
from dbmodels import Course, AltDesc, Section
from dbsearch import *

from dbmisc import get_depts, next_alt_desc_id
from stringhelp import listify, id_to_url, id_from_url
from history import History

from forms import CourseQueryForm, AltDescForm

import datetime, time
from collections import OrderedDict

dbsession = loadSession()

#custom render template, so we don't need to remember to put in history
#can handle history if need
#(used for course pages, so they include themselves in history)
def render_template(*args,**kwargs):
    if 'history' not in kwargs:
        history = History()
        return flask_render_template(*args, history=history, **kwargs)
    else:
        return flask_render_template(*args, **kwargs)

@app.route('/coursefinder')
def main_page():
    print request.method
    form = CourseQueryForm()
    return render_template('form.html', form=form)

@app.route("/coursefinder/results")
def results_page(methods=['POST','GET']):
    course_query_form = CourseQueryForm()
    args = preprocess_args(request.args)
    results = search(dbsession,**args)
    if len(results):
        return render_template("results.html",
                               courses = results)
    else:
        return render_template("no_results.html")

@app.route('/catalog')
def catalog():
    dept_list = sorted(get_depts(dbsession))
    return render_template('catalog.html',depts=dept_list)

@app.route('/catalog/<dept>')
def dept_page(dept):
    dept = dept.upper()

    res = dbsession.query(Course)
    course_list = list(res.filter(Course.dept == dept))
    course_list.sort(key = lambda c: c.id)

    return render_template('dept.html',dept=dept,courses=course_list)

@app.route('/catalog/<dept>/<course_id>')
def course_page(dept, course_id):
    try: #format id, else tell user that id is invalid
        formatted_id = id_from_url(course_id)
    except ValueError:
        return '\''+course_id+'\' is not a valid course id.'

    try:
        res = dbsession.query(Course)
        course = res.filter(Course.id == formatted_id).one()
    except:
        return 'Course \'' + course_id + '\' does not exist.'

    #get alt descs for course
    res = dbsession.query(AltDesc)
    alt_desc_list = list(res.filter(AltDesc.course_id == formatted_id))

    #get alt descs for courses that are the same (like CS220 and MATH220)
    #and concatenate them together
    for same_course in listify(course.same_as):
        additional_alt_descs = dbsession.query(AltDesc).filter(AltDesc.course_id == same_course)
        alt_desc_list += list(additional_alt_descs)

    #remove unapproved alt descs
    alt_desc_list = filter(lambda alt_desc: alt_desc.approved, alt_desc_list)

    sections = dbsession.query(Section).\
                         filter( Section.course_id == formatted_id )
    term_offerings = OrderedDict()
    for term in terms:
        term_offerings[term] = sections.filter(Section.term==term)
        term_offerings[term] = list(term_offerings[term])

    course = search(dbsession, course_id = course.id)
    course = course[course.keys()[0]]

    form = AltDescForm()

    #Appends course title to history
    history = History()
    history.add(course)
    #Sets history cookie
    resp = make_response( render_template("course.html",
                                          course=course,
                                          form=form,
                                          alt_descs=alt_desc_list,
                                          terms=term_offerings,
                                          history=history) )
    resp.set_cookie('history', str(history), max_age=365*24*60*60) #cookie lasts a year
    return resp

@app.route('/catalog/<dept>/<course_id>/submit')
def submit_alt_desc(dept, course_id, methods=['POST','GET']):
    formatted_id = id_from_url(course_id)
    form = AltDescForm(request.args)
    if form.validate():
        print 'form validated'
        alt_desc = AltDesc(next_alt_desc_id(dbsession),
                           False,
                           datetime.date.fromtimestamp(time.time()),
                           form.content.data,
                           str(formatted_id))
        db.session.add(alt_desc)
        db.session.commit()
        flash('Thanks for submitting an alternative description')
    return redirect('/catalog/'+dept+"/"+course_id)

@app.route('/about')
def about_page():
    return render_template('about.html')

@app.route('/api')
def api(methods=['POST','GET']):
    args = preprocess_args(request.args)
    data = search(dbsession,**args)
    return jsonify(**data)

@app.route('/api/docs')
def api_docs():
    return render_template('api_docs.html')

@app.route('/')
def go_to_main_page():
    return redirect('/coursefinder')

if __name__ == "__main__":
    app.run(debug=True)
