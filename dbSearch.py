from config import *

from sqlalchemy import create_engine, MetaData, Table
from sqlalchemy.orm import mapper, sessionmaker
 
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


       
def search( title = None, dept = None, gen_eds = None, prereqs = None, professors = None, id = None, ses = None):
    '''This method essentially employs the accumlutator method to create a string that looks like an sqlAlchemy query. The string is evaluated in return statement, and a list of DB entries that match the query is returned'''
    temp = locals() #makes a dictionary of all of the parameters
    params = dict(temp) # creates a new dictionary of parameters, this one doesn't change as you add new locals.
    if dept:
        res = ses.filter(CourseDB.dept == dept.upper())
    else:
        res = ses
    string = "" 
    for key in params:
        if key == "title":
            pass #ignore titles for now -- they are handled by keyword_sort
            #params[key] = params[key].title()
        elif params[key] and type(params[key]) is str and key != 'dept':
            string += ".filter(CourseDB."+key+".like('%"+params[key]+"%'))" #Some bugs occuring due to the "like()" function

    result ="res" + string + ".all()"
    
    print("SEARCH QUERY: "+ eval('result')) #Prints final sqlAlchemy query
    print("")
    
    return eval(result) #Evaluates that query.


def results_page_search(dbsession,request):
    res = dbsession.query(CourseDB)
    gen_eds_list = request.args.getlist("gen_eds")
    print(gen_eds_list, "wow!")
    search_string = "search("
    for i in request.args:
        if i != "gen_eds":
            search_string += i+"="+"'"+request.args[i]+"'"+", "

    new_search_string = ""
    to_become_set = []
    if len(gen_eds_list) == 0:
        search_string += "ses = res)"
        to_become_set = eval(search_string)
    for gen_ed in gen_eds_list:
        new_search_string = str(search_string+"gen_eds = "+"'"+gen_ed+"'" + ", ses = res)")
        temp = eval(new_search_string)
        print(new_search_string, "WHAT IS GOING ON...?")
        print(temp)
        to_become_set += temp
    
    result = set(to_become_set)
    print("")
#    print(result)
    return sorted(list(result))

def api_search(dbsession,request):
    res = dbsession.query(CourseDB)
    gen_eds_list = request.args.getlist("gen_eds")
    
    search_string = "search("
    for i in request.args:
        if i != "gen_eds":
            search_string += i+"="+"'"+request.args[i]+"'"+", "

    new_search_string = ""
    to_become_set = []
    if len(gen_eds_list) == 0:
        search_string += "ses = res)"
        to_become_set = eval(search_string)
    for gen_ed in gen_eds_list:
        new_search_string = str(search_string+"gen_eds = "+"'"+gen_ed+"'" + ", ses = res)")
        temp = eval(new_search_string)
        print(new_search_string, "WHAT IS GOING ON...?")
        print(temp)
        to_become_set += temp #this gets us our combination of lists. 
    to_become_dict =list(set(to_become_set))
    result = {}
    for course in to_become_dict:
        result[course.id] = {'title':course.title, 'number':course.number, 'id':course.id, 'dept':course.id, 'desc':course.desc, 'same_as':course.same_as, 'gen_eds':course.gen_eds, 'hours':course.hours}#, 'professors':course.professors}
   
    

    return result
    
    

#----------------------------------------------------------------------


 
if __name__ == "__main__":
    
    session = loadSession()
    
    #res = session.query(CourseDB.title, CourseDB.gen_eds, CourseDB.dept)
    
    res = session.query(CourseDB.title) #Note: In the end, we'll want the query so simply return the class.
    print("")
    print("")
#    print(search(title = "", dept = "", gen_eds = "", prereqs = "",  ses = res))
    print("")
    print("")
    print(search(dept = "CSSSS", ses = res))
    print("")
    print("")
 #   print(search(id = "MATH 110", ses = res)) 


    
    
