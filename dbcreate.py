from config import *
import sys, json
from dbmodels import Course, AltDesc, GenEd
from coursedata import get_course_data

def main():
    update = False
    for arg in sys.argv:
        if arg == '-u':
            update = True

    if not update:
        try:
            course_data_file = open('course_data.json','r')
            course_data = json.load(course_data_file,'utf8')
            course_data_file.close()
        except IOError:
            update = True

    if update:
        print 'Getting data from internet'
        course_data = get_course_data(quiet=False)
        print 'Data collected'
        print 'Saving data in \'course_data.json\''
        course_data_file = open('course_data.json','w')
        json.dump(course_data,course_data_file)
        course_data_file.close()
        print 'Data saved'
    
    db.drop_all()
    db.create_all()
    
    count = 0
    total = float(len(course_data))
    prev_percent = -5
    print 'Creating database'
    #make the db

    print 'Loading gen eds'
    gen_eds = []
    for course_id in course_data:
        for gen_ed in course_data[course_id]['gen_eds'].split(', '):
            if gen_ed not in gen_eds:
                gen_eds.append(gen_ed)

    print 'Adding gen eds to database'
    gen_ed_dict = {}
    for gen_ed in gen_eds:
        g = GenEd(abbr=gen_ed)
        db.session.add(g)
        if gen_ed not in gen_ed_dict:
            gen_ed_dict[gen_ed] = g
    print 'Gen eds added'

    print 'Adding courses to database'
    for course_id in course_data:
        course = course_data[course_id]
        #gen_eds = course['gen_eds'].split(', ')

        c = Course(title = course["title"],
                   dept = course["dept"],
                   number = course["number"],
                   desc = course["desc"],
                   hours = course["hours"],
                   prereqs = course["prereqs"],
                   same_as = course["same_as"],
                   id = course["id"])

        for gen_ed_abbr in course['gen_eds'].split(', '):
            gen_ed_dict[gen_ed_abbr].courses.append(c)
            db.session.add(gen_ed_dict[gen_ed_abbr])
            
        db.session.add(c)

        count += 1
        cur_percent = (count/total*100)
        cur_percent -= cur_percent % 5
        if cur_percent != prev_percent:
            print str(int(cur_percent))+' %'
            prev_percent = cur_percent
        
    db.session.commit()
    print 'COMPLETE'

if __name__ == "__main__":
    main()
