from config import *

#I first, I need to be able to access my database


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
       
def search( title = None, dept = None, gen_eds = None, prereqs = None, professors = None, ses = None):
    '''This method essentially employs the accumlutator method to create a string that looks like an sqlAlchemy query. The string is evaluated in return statement, and a list of DB entries that match the query is returned'''
    temp = locals() #makes a dictionary of all of the parameters
    params = dict(temp) # creates a new dictionary of parameters, this one doesn't change as you add new locals.
    
    res = ses
    
    string = "" 
    for key in params:
        
        if params[key] and type(params[key]) is str :
            string += ".filter(CourseDB."+key+".like('%"+params[key]+"%'))" #Some bugs occuring due to the "like()" function
                
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
    print(search(title = "Introduction", dept = "Rel", gen_eds = "BL", ses = res))
    print("")
    print("")
    print(search(gen_eds = "HBSSM", ses = res))
    print("")
    print("")
    print(search(dept = "Math", ses = res)) 


    
    
