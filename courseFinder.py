from config import *

class MyForm(Form):
    name = TextField('Name',[validators.Length(min=4, max=25)])
    department = BooleanField('Spring 2014')

class CourseQueryForm(Form):
    dept = TextField('Department',[validators.Length(min=2, max=5)])
    number = TextField('Course Number',[validators.Length(min=3, max=4)])
    title = TextField('Course Title')
    gen_ed_bl = BooleanField('BL')
    gen_ed_hb = BooleanField('HB')
    gen_ed_hbssm = BooleanField('HBSSM')
    gen_ed_he = BooleanField('HE')
    gen_ed_hept = BooleanField('HEPT')
    gen_ed_hist = BooleanField('Hist')
    gen_ed_intcl = BooleanField('Intcl')
    gen_ed_nwl = BooleanField('NWL')
    gen_ed_nwnl = BooleanField('NWNL')
    gen_ed_quant = BooleanField('Quant')
    gen_ed_rel = BooleanField('Rel')
    gen_ed_skl = BooleanField('Skl')
    gen_ed_wel = BooleanField('Wel')

@app.route('/courseFinder', methods=['POST', 'GET'])
def forms_page():
    if request.method == 'GET':
        print 'Request == \'GET\''
        print 'request.args:', str([key+': '+request.args[key]
                                    for key in request.args.keys()])
        form = MyForm(request.args)
    else:
        print 'not Request == \'GET\''
        form = MyForm()

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
