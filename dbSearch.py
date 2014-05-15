from config import *

from sqlalchemy import create_engine, MetaData, Table
from sqlalchemy.orm import mapper, sessionmaker
 
class CourseDB(object):
    pass
 
#----------------------------------------------------------------------
def loadSession():
    """This function generates a session, with which you can make queries to the database."""    
    
    engine = create_engine(dbPath) #, echo=True)  #<<< let's you see the database commands in stdout
 
    metadata = MetaData(engine)
    
    courses = Table('courses', metadata, autoload=True)
    mapper(CourseDB, courses)
 
    Session = sessionmaker(bind=engine)
    session = Session()
    return session


       
def search( title = None, dept = None, gen_eds = None, prereqs = None, professors = None, id = None, ses = None):
    '''This method essentially employs the accumlutator method to create a string that looks like an sqlAlchemy query. The string is evaluated in return statement, and a list of DB entries that match the query is returned'''
    temp = locals() #makes a dictionary of all of the parameters
    params = dict(temp) # creates a new dictionary of parameters, this one doesn't change as you add new locals.
    
    res = ses
    
    string = "" 
    for key in params:
        print(params[key])
        if params[key] and type(params[key]) is str:# and key != 'dept':
            string += ".filter(CourseDB."+key+".like('%"+params[key]+"%'))" #Some bugs occuring due to the "like()" function
        
        #if key == 'dept':
        #    string += ".filter(CourseDB."+key+"='"+params[key]+"')"
        #    print("here")

        #maybe have an if statement for everything but dept. These calls would have the "like()" function
        
                
    result ="res" + string + ".all()"
    
    print("SEARCH QUERY: "+ eval('result')) #Prints final sqlAlchemy query
    print("")
    
    return eval(result) #Evaluates that query.

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


    
    
