from config import *
from dbSearch import *

session = loadSession()



class CourseQueryForm(Form):
    dept = TextField('Department',[validators.Length(min=2, max=5)], id="dept")
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




@app.route("/coursefinder/results",methods=['POST','GET'])
def results_page():
    course_query_form = CourseQueryForm(request.args, csrf_enabled=False)
    res = session.query(CourseDB)
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

@app.route('/coursefinder')
def main_page( methods=['POST','GET']):
    print request.method
    course_query_form = CourseQueryForm(csrf_enabled=False)
    print course_query_form.validate()
    return render_template('form.html', form=course_query_form)


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

