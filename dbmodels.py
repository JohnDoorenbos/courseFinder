from config import *

#association table
gen_ed_fulfillments = db.Table('gen_ed_fulfillments',
                               db.Column('gen_ed_abbr', db.Text, db.ForeignKey('gen_eds.abbr')),
                               db.Column('course_id',db.Text, db.ForeignKey('courses.id')))

class Course(db.Model):
    __tablename__ = "courses"
    title = db.Column(db.Text)
    dept = db.Column(db.Text)
    number = db.Column(db.Text)
    desc  = db.Column(db.Text)
    hours = db.Column(db.Text)
    gen_eds = db.relationship("GenEd",secondary = gen_ed_fulfillments, backref='courses')#db.Column(db.Text)
    prereqs = db.Column(db.Text)
    id = db.Column(db.Text, primary_key = True)
    same_as = db.Column(db.Text)
    alt_descs = db.relationship("AltDesc")
    def __init__(self, title, dept, number, desc, prereqs, id, hours, same_as):
        self.title = title
        self.dept = dept
        self.number = number
        self.desc = desc
        self.hours = hours
        self.prereqs = prereqs
        self.id = id
        self.same_as = same_as
        self.gen_eds = []
    def __str__(self):
        return(self.title +" " + self.id + " " + self.gen_eds)

class AltDesc(db.Model):
    __tablename__ = "alt_descs"
    alt_desc_id = db.Column(db.Integer, primary_key = True)
    approved = db.Column(db.Boolean)
    date_submitted = db.Column(db.Date)
    content = db.Column(db.Text)
    course_id = db.Column(db.Text, db.ForeignKey('courses.id'))

    def __init__(self, alt_desc_id, approved,
                 date_submitted, content, course_id):
        self.alt_desc_id = alt_desc_id
        self.approved = approved
        self.date_submitted = date_submitted
        self.content = content
        self.course_id = course_id

class GenEd(db.Model):
    __tablename__ = 'gen_eds'
    abbr = db.Column(db.Text, primary_key = True)
    #courses = db.relationship('Course', secondary=gen_ed_fulfillments)

    def __init__(self, abbr):
        self.abbr = abbr
