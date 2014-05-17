from config import *
from coursedata import get_course_data
def main():
    course_data = get_course_data()
    
    db.drop_all()
    db.create_all()
    
#make the db
    for course in course_data:
        c1  = Course(title = course["title"], dept = course["dept"], number = course["number"], desc = course["desc"],  hours = course["hours"], gen_eds = course["gen_eds"], prereqs = course["prereqs"], professors = [], same_as = course["same_as"], id = course["id"])
        print(c1)
        db.session.add(c1)
        db.session.commit()

    return str(course_data)
if __name__ == "__main__":
    main()
