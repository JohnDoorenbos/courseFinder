from config import *
import sys, json
from dbmodels import Course, AltDesc, GenEd, Section
from coursedata import get_course_data, get_section_data

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
    
    print 'Initializing database'
    db.drop_all()
    db.create_all()
    
    print 'Adding courses to database'
    gen_ed_dict = {}
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
            if gen_ed_abbr not in gen_ed_dict:
                gen_ed_dict[gen_ed_abbr] = GenEd(abbr=gen_ed_abbr)
                db.session.add(gen_ed_dict[gen_ed_abbr])
            gen_ed_dict[gen_ed_abbr].courses.append(c)
            db.session.add(gen_ed_dict[gen_ed_abbr])
            
        db.session.add(c)

    print 'Adding sections to database'
    section_data = get_section_data('2014FA')
    for section_id in section_data:
        section = section_data[section_id]
        s = Section( section_id = section_id,
                     course_id = section['course_id'],
                     min_credits = int(section['min_credits']),
                     max_credits = int(section['max_credits']),
                     title = section['title'],
                     primary_instructor =section['primary_instructor'],
                     other_instructors = section['other_instructors'],
                     room = section['room'],
                     start_time = section['start_time'],
                     end_time = section['end_time'],
                     days = section['days'],
                     seven_weeks = section['seven_weeks'] )
        db.session.add(s)

    db.session.commit()
    print 'COMPLETE'

if __name__ == "__main__":
    main()
