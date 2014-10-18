from config import *
from coursedata import get_course_data

def main():
    print 'Getting data from internet'
    course_data = get_course_data()
    print 'Data collected'
    
    db.drop_all()
    db.create_all()
    
    count = 0
    total = float(len(course_data))
    prev_percent = -5
    print 'Creating database\n0 %'
    #make the db

    for course in course_data:
        c1  = Course(title = course["title"], dept = course["dept"], number = course["number"], desc = course["desc"],  hours = course["hours"], gen_eds = course["gen_eds"], prereqs = course["prereqs"], professors = [], same_as = course["same_as"], id = course["id"])
        
        db.session.add(c1)
        db.session.commit()

        count += 1
        cur_percent = (count/total*100)
        cur_percent -= cur_percent % 5
        if cur_percent != prev_percent:
            print str(int(cur_percent))+' %'
            prev_percent = cur_percent
        
    print 'COMPLETE'

if __name__ == "__main__":
    main()
