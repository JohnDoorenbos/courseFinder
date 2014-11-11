from config import *
from dbsearch import loadSession, AltDescDB, CourseDB

dbsession = loadSession()

def approve_alt_descs():
    unapproved_alt_descs = list(dbsession.query(AltDescDB).filter(AltDescDB.approved == False))
    for alt_desc in unapproved_alt_descs:
        print ''
        print 'Submitted: %s' % alt_desc.date_submitted
        print 'Content: %s' % alt_desc.content
        command = ''
        while not (command == 'A' or command == 'D' or command == 'S'):
            command = raw_input('Enter \'A\' to approve, \'D\' to delete, or \'S\' to save for later\n> ')
        if command == 'A':
            alt_desc.approved = True
            dbsession.add(alt_desc)
        elif command == 'D':
            dbsession.delete(alt_desc)
        elif command == 'S':
            pass #do nothing
    dbsession.commit()
