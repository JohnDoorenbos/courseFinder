from config import *

class MyForm(Form):
    name = TextField('Name',[validators.Length(min=4, max=25)])
    department = BooleanField('Spring 2014')

class CourseQueryForm(Form):
    dept = TextField('Department',[validators.Length(min=2, max=5)])
    number = TextField('Course Number',[validators.Length(min=3, max=4)])
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

@app.route('/coursefinder', methods=['POST', 'GET'])
def forms_page():
    if request.method == 'GET':
        print 'Request == \'GET\''
        print 'request.args:', str([key+': '+request.args[key]
                                    for key in request.args.keys()])
        form = CourseQueryForm(request.args)
    else:
        print 'not Request == \'GET\''
        form = CourseQueryForm()

    if form.validate():
        print 'form validated'
        return 'Hello, validated form!'
    else:
        print 'form not validated'
        if form.errors:
            for error in form.errors:
                print str(error) + ': ' + str(form.errors[error])
        return render_template('form.html',form = form)

@app.route("/results")
def results_page():
    return render_template("results.html")

if __name__ == "__main__":
    app.run(debug=True)
