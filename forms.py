from config import *

class CustomForm(Form):
    def remove_csrf(self):
        self.__delitem__('csrf_token')
        self.csrf_enabled = False
        return self

class CourseQueryForm(CustomForm):
    dept = TextField('Department', id="dept")
    title = TextField('Keywords', id="title")
    gen_eds = SelectMultipleField('Gen Ed Fulfillments',
                                  choices=[('',''),
                                           ('BL','BL'),
                                           ('HB','HB'),
                                           ('HBSSM','HBSSM'),
                                           ('HE','HE'),
                                           ('HEPT','HEPT'),
                                           ('Hist','Hist'),
                                           ('Intcl','Intcl'),
                                           ('NWL','NWL'),
                                           ('NWNL','NWNL'),
                                           ('Quant','Quant'),
                                           ('Rel','Rel'),
                                           ('Skl','Skl'),
                                           ('Wel','Wel')], id="gen_eds")

class ReviewForm(CustomForm):
    stars = IntegerField('Rating (1-5)', [validators.DataRequired(),
                                          validators.NumberRange(1,5)],
                         id="stars")
    content = TextAreaField('Content',id="content")
