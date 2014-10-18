import re

def listify(s):
    if s == 'N/A':
        return []
    else:
        return [i.strip() for i in s.split(',')]

def id_from_url(course_id):
    '''takes an id like 'cs200' and return 'CS 200'
    mostly used for preparing ids from urls to be used in the database'''
    match = re.match('^([A-Z]+)(\d{3}(-\d{3})*.?)$',course_id.upper())
    if match:
        dept = str(match.group(1))
        number = str(match.group(2)).replace('-',', ')
        return dept + ' ' + number
    else:
        raise(ValueError,'\''+course_id+'\' is not a valid course id')


def id_to_url(course_id):
    '''takes an id like 'CS 200' and returns 'cs200'
    for reviews from the database to be used in a url'''
    return str(course_id.replace(', ','-').remove(' '))
