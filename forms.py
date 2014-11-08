from config import *
from flask_wtf import Form
from wtforms import IntegerField, TextAreaField, TextField, BooleanField, SubmitField, SelectMultipleField, validators 

class CustomForm(Form):
    def __init__(self,*args):
        super(CustomForm,self).__init__(*args)
        self.__delitem__('csrf_token')
        self.csrf_enabled = False

class CourseQueryForm(CustomForm):
    dept = TextField('Department', id="dept")
    keywords = TextField('Keywords', id="keywords")
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

class AltDescForm(CustomForm):
    content = TextAreaField('Content',
                            [validators.DataRequired()],
                            id="content")
