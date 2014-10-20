from config import *

from sqlalchemy import create_engine, MetaData, Table
from sqlalchemy.orm import mapper, sessionmaker

import json
from collections import OrderedDict
from stringhelp import listify
 
class CourseDB(object):
    pass
class ReviewDB(object):
    pass

#----------------------------------------------------------------------

def loadSession():
    """This function generates a session, with which you can make queries to the database."""    
    
    engine = create_engine(dbPath) #, echo=True)  #<<< let's you see the database commands in stdout
 
    metadata = MetaData(engine)
    
    courses = Table('courses', metadata, autoload=True)
    mapper(CourseDB, courses)
 
    reviews = Table('reviews',metadata, autoload=True)
    mapper(ReviewDB, reviews)
    
    Session = sessionmaker(bind=engine)
    session = Session()
    return session

def preprocess_args(args):
    if 'dept' in args:
        dept = args['dept'].upper()
    else:
        dept = None

    if 'keywords' in args:
        keywords = args['keywords'].lower().split()
    else:
        keywords = []

    if 'gen_eds' in args:
        gen_eds = args.getlist('gen_eds')
        if '' in gen_eds:
            gen_eds.remove('') #if nothing is entered in the form, gen_eds is [u''], which returns no results. This fixes that

    else:
        gen_eds = []
    auto_add_overqualifying(gen_eds,args)

    if len(keywords):
        sort = 'keyword'
    else:
        sort = 'alpha'

    return {'dept':dept,
            'keywords':keywords,
            'gen_eds':gen_eds,
            'sort':sort}

def auto_add_overqualifying(gen_eds,args={}):
    if 'auto_hbssm' in args:
        auto_hbssm = eval(args['auto_hbssm'])
    else:
        auto_hbssm = True

    if 'auto_hept' in args:
        auto_hept = eval(args['auto_hept'])
    else:
        auto_hept = True

    if 'auto_nwl' in args:
        auto_nwl = eval(args['auto_nwl'])
    else:
        auto_nwl = False

    if auto_hbssm:
        if 'HBSSM' not in gen_eds and 'HB' in gen_eds:
            gen_eds.append('HBSSM')
    if auto_hept:
        if 'HEPT' not in gen_eds and 'HE' in gen_eds:
            gen_eds.append('HEPT')
    if auto_nwl:
        if 'NWL' not in gen_eds and 'NWNL' in gen_eds:
            gen_eds.append('NWL')

def search(session,dept=None, keywords=[], gen_eds=[], sort=None):
    res = session.query(CourseDB)

    if dept:
        res = res.filter(CourseDB.dept == dept)

    if gen_eds:
        new_res = None
        for gen_ed in gen_eds:
            only_str = gen_ed
            first_str = gen_ed + ',%' #this gen_ed starts list
            mid_str = '% ' + gen_ed + ',%' #in middle of lsit
            last_str = '% ' + gen_ed #at end of list
            gen_ed_only = res.filter(CourseDB.gen_eds.like(only_str))
            gen_ed_first = res.filter(CourseDB.gen_eds.like(first_str))
            gen_ed_mid = res.filter(CourseDB.gen_eds.like(mid_str))
            gen_ed_last = res.filter(CourseDB.gen_eds.like(last_str))
            temp_res = gen_ed_only.\
                       union(gen_ed_first).\
                       union(gen_ed_mid).\
                       union(gen_ed_last)
            if new_res: #new_res exists, so combine with temp_res
                new_res = temp_res.union(new_res)
            else: #new_res is None, so make new_res temp_res
                new_res = temp_res
        res = new_res

    result_dict = {}
    for course in res:
        result_dict[course.id] = {'id':course.id,
                          'number':course.number,
                          'dept':course.dept,
                          'hours':course.hours,
                          'title':course.title,
                          'desc':course.desc,
                          'same_as':course.same_as,
                          'prereqs':course.prereqs,
                          'gen_eds':course.gen_eds}

    for course in result_dict:
        count = 0
        for word in keywords:
            count += result_dict[course]['title'].lower().count(word)
            count += result_dict[course]['desc'].lower().count(word)
        result_dict[course]['keyword_count'] = count

        gen_ed_list = listify(result_dict[course]['gen_eds'])
        result_dict[course]['gen_ed_count'] = len(gen_ed_list)
        count = 0
        for gen_ed in gen_eds:
            if gen_ed in gen_ed_list:
                count += 1
        result_dict[course]['searched_gen_ed_count'] = count

    if keywords:
        for course_id in result_dict.keys():
            if result_dict[course_id]['keyword_count'] == 0:
                del result_dict[course_id]

    if sort:
        if sort == 'alpha':
            sorted_keys = sorted(result_dict)

        elif sort == 'keyword':
            sorted_keys = sorted(result_dict,
                                 key = lambda k: result_dict[k]['keyword_count'],
                                 reverse=True)

        sorted_results = OrderedDict()
        for course_id in sorted_keys:
            sorted_results[course_id] = result_dict[course_id]

        return sorted_results

    else:
        return result_dict

#----------------------------------------------------------------------
 
if __name__ == "__main__":
    session = loadSession()
    result = search(session,keywords=['plato','aristotle','homer','classical','hellenic','roman republic','rome','athens', 'roman', 'greek','greece'],sort='keyword')

    for course_id in result:
        print course_id,result[course_id]['keyword_count']
