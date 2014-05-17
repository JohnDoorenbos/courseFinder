from config import *
from coursedata import get_course_data
def main():
    course_data = get_course_data()
    
    db.drop_all()
    db.create_all()
    
#make the db
    for course in course_data:
        c1  = Course(title = course["title"], dept = course["dept"], number = course["number"], desc = course["desc"],  hours = course["hours"], gen_eds = course["gen_eds"], prereqs = course["prereqs"], professors = [], same_as = course["same_as"], id = course["id"])
        db.session.add(c1)
        db.session.commit()
        '''
        c1 = Course(title = "Intro to Bib", dept = "Religion", number = "3025", desc = "NOTHING TO KNOW", gen_eds = "REL", prereqs = "None", professors = [], hours = "4", same_as = "None", id = "CS 4465")
        
        c2 = Course(title = "Global Politics", dpt = "Politics", number = "3467", desc = "Fun class!", gen_eds = "POLS", prereqs = "None", professors = [], hours = "2", same_as = "Cows", id = "POLS 4465")
        '''
#db.session.add(c1)
        
#db.session.commit()

if __name__ = "__main__":
    main()
