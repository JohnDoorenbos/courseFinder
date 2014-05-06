from config import *
from coursedata import get_course_data

courses = get_course_data()

course_offerings = db.Table('course_offerings',
                            db.Column('course_id',db.Text, db.ForeignKey('courses.id')),
                            db.Column('prof_name',db.Text, db.ForeignKey('professors.name'))
)


class Course(db.Model):
    __tablename__ = "courses"
    title = db.Column(db.Text)
    dpt = db.Column(db.Text)
    number = db.Column(db.Text)
    desc  = db.Column(db.Text)
    hours = db.Column(db.Text)
    gen_eds = db.Column(db.Text)
    prereqs = db.Column(db.Text)
    id = db.Column(db.Text, primary_key = True)
    professors = db.relationship("Professor",secondary = course_offerings)
    same_as = db.Column(db.Text)
    def __init__(self, title, dpt, number, desc, gen_eds, prereqs, id, professors, hours, same_as):
        self.title = title
        self.dpt = dpt
        self.number = number
        self.desc = desc
        self.hours = hours
        self.gen_eds = gen_eds
        self.prereqs = prereqs
        self.id = id
        self.professors = professors
        self.same_as = same_as
    
class Professor(db.Model):
    __tablename__ = "professors"
    name =  db.Column(db.Text, primary_key = True)
    bio =  db.Column(db.Text)
    department =  db.Column(db.Text)
    courses = db.relationship("Course", secondary = course_offerings)
    
    def __init__(self,name, bio, department, courses):
        self.name = name
        self.bio = bio
        self.department = department
        self.courses = courses

db.drop_all()
db.create_all()

#make the db 


c1 = Course(title = "Intro to Bib", dpt = "Religion", number = "3025", desc = "NOTHING TO KNOW", gen_eds = "REL", prereqs = "None", professors = [], hours = "4", same_as = "None", id = "CS 4465")

c2 = Course(title = "Global Politics", dpt = "Politics", number = "3467", desc = "Fun class!", gen_eds = "POLS", prereqs = "None", professors = [], hours = "2", same_as = "Cows", id = "POLS 4465")

db.session.add(c1)

db.session.commit()
