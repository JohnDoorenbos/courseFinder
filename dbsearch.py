from config import *

from sqlalchemy import create_engine, MetaData, Table
from sqlalchemy.orm import mapper, sessionmaker
from dbmodels import Course, AltDesc, GenEd

import json
from collections import OrderedDict
from stringhelp import listify
 
def loadSession():
    """This function generates a session, with which you can make queries to the database."""    
    
    engine = create_engine(dbPath) #, echo=True)  #<<< let's you see the database commands in stdout
 
    metadata = MetaData(engine)
    
    courses = Table('courses', metadata, autoload=True)
    alt_descs = Table('alt_descs',metadata, autoload=True)
    gen_eds = Table('gen_eds', metadata, autoload=True)
    
    Session = sessionmaker(bind=engine)
    session = Session()
    session._model_changes = {}
    return session

def preprocess_args(args):
    if 'course_id' in args:
        course_id = id_from_url(args['course_id'])
    else:
        course_id = None

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

    return {'course_id':course_id,
            'dept':dept,
            'keywords':keywords,
            'gen_ed_abbrs':gen_eds,
            'sort':sort}

def auto_add_overqualifying(gen_eds,args={}):
    if 'auto_hbssm' in args:
        auto_hbssm = eval(args['auto_hbssm'])
    else:
        auto_hbssm = True #default include

    if 'auto_hept' in args:
        auto_hept = eval(args['auto_hept'])
    else:
        auto_hept = True #default include

    if 'auto_nwl' in args:
        auto_nwl = eval(args['auto_nwl'])
    else:
        auto_nwl = False #default not include (some people avoid labs)

    if auto_hbssm:
        if 'HBSSM' not in gen_eds and 'HB' in gen_eds:
            gen_eds.append('HBSSM')
    if auto_hept:
        if 'HEPT' not in gen_eds and 'HE' in gen_eds:
            gen_eds.append('HEPT')
    if auto_nwl:
        if 'NWL' not in gen_eds and 'NWNL' in gen_eds:
            gen_eds.append('NWL')

def search(session, course_id=None, dept=None, keywords=[], gen_ed_abbrs=[], sort=None):
    res = session.query(Course)

    if course_id:
        res = res.filter(Course.id == course_id)

    if dept:
        res = res.filter(Course.dept == dept)

    if gen_ed_abbrs:
        new_res = None
        for abbr in gen_ed_abbrs:
            temp_res = res.filter(Course.gen_eds.any(abbr=abbr))
            if new_res: #new_res exists, so combine with temp_res
                new_res = temp_res.union(new_res)
            else: #new_res is None, so make new_res temp_res
                new_res = temp_res
        res = new_res

    result_dict = {}
    for course in res:
        #course_gen_eds = res.filter(Course.gen_eds.all())
        result_dict[course.id] = {'id':course.id,
                          'number':course.number,
                          'dept':course.dept,
                          'hours':course.hours,
                          'title':course.title,
                          'desc':course.desc,
                          'same_as':course.same_as,
                          'prereqs':course.prereqs,
                          'gen_eds': ', '.join( [gen_ed.abbr for gen_ed in session.query(GenEd).filter(GenEd.courses.any(id=course.id)) ] ) }

    for course in result_dict:
        count = 0
        for word in keywords:
            count += result_dict[course]['title'].lower().count(word)
            count += result_dict[course]['desc'].lower().count(word)
        result_dict[course]['keyword_count'] = count

        gen_ed_list = listify(result_dict[course]['gen_eds'])
        result_dict[course]['gen_ed_count'] = len(gen_ed_list)
        count = 0
        for abbr in gen_ed_abbrs:
            if abbr in gen_ed_list:
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
