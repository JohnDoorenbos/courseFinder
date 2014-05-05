class Course(db.Model):
    __table__ = "courses"
    name = db.column(db.Text, primary_key = True)
    department = db.column(db.Text)  #not sure if any of these can be stored as lists or not. currently strings.
    number = db.column(db.Integer)
    description  = db.column(db.Text)
    gen_ed_requirements = db.column(db.Text)
    pre_reqs = db.column(db.Text)
    professors = de.relationship("Professor",secondary = course_offerings)
    
    def __init__(self, name, department, number, description, gen_ed_requirements, pre_reqs, professors):
        self.name = name
        self.department = depart
        self.number = number
        self.description = description
        self.gen_ed_requirements = gen_ed_requirements
        self.pre_reqs = pre_reqs
        self.professors = professors

class Professor(db.Model):
    __table__ = "professors"
    name =  db.column(db.Text, primary_key = True)
    bio =  db.column(db.Text)
    department =  db.column(db.Text)
    courses = db.relationship("Course", secondary = course_offerings)
    
    def __init__(self,name, bio, department, courses):
        self.name = name
        self.bio = bio
        self.department = department
        self.courses = courses




course_offerings = db.Table('course_offerings',
                            db.Column('course_name',db.Integer, db.ForeignKey('courses.name')),
                            db.Column('prof_name',db.Integer, db.ForeignKey('professors.name'))
                                
