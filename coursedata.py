import urllib2, re, bs4

def create_url_list():
    '''Creates the list of urls for each departments course listings'''
    department_ids = list(range(3890,3941)) + [4215,4229]
    return ['http://www.luther.edu/catalog/' + str(department_id) + '.htm'
            for department_id in department_ids]

def parse_coursetitle(text,course):
    '''gets the department (ie BIO, CS, etc), course number and title
    from text. It stores these in the 'dept', 'number' and 'title'
    keys respectively'''

    match = re.match('^([a-zA-Z]+) (\d{3}[\d/, ]*.?) (.*?)$', text)
    course['id'] = match.group(1) + ' ' + match.group(2)
    course['dept'] = match.group(1)
    course['number'] = match.group(2)
    course['title'] = match.group(3)

def parse_credithours(text,course):
    '''adds the 'hours' key to course'''
    course['hours'] = text

def parse_coursedescriptions(text,course):
    '''gets the course description and the prereqs (if any), courses it's
    the same as (if any), and gened fulfillments (if any). It stores these
    in the 'desc', 'prereqs', 'sameas', and 'geneds' keys respectively'''

    course['raw_desc'] = text

    #checks for most complicated matches first, assigning others to None
    match1 = re.match('^(.*) Prerequisites?: (.*?)\..*?\((.*)\) ?$', text)
    if match1:
        match2 = None
        match3 = None
    else:
        match2 = re.match('^(.*?) ?\((Same.*)\)$ ?', text) #something wrong!!!
        if match2:
            match3 = None
            match4 = None
        else:
            match3 = re.match('^(.*) ?\((.*?)\)$ ?', text)
            if match3:
                match4 = None
            else:
                match4 = re.match('^(.*) Prerequisites?: (.*?) ?\.', text)

    if match1: #has prereqs, and sameas and/or geneds
        match = match1
        course['desc'] = match.group(1)
        course['prereqs'] = match.group(2)

        if ')' in match.group(3):
            course['same_as'] = match.group(3)[ 8 : match.group(3).index(')') ]
            course['gen_eds'] = match.group(3)[ match.group(3).index('(')+1 : ]
        elif 'Same' in match.group(3):
            course['same_as'] = match.group(3)[8:]
        else:
            course['gen_eds'] = match.group(3)

    elif match2: #no prereqs, but has sameas and maybe geneds
        match = match2
        course['desc'] = match.group(1)
        if ')' in match.group(2):
            course['same_as'] = match.group(2)[ 8 : match.group(2).index(')') ]
            course['gen_eds'] = match.group(2)[ match.group(2).index('(')+1 : ]
        else:
            course['same_as'] = match.group(2)[8:]

    elif match3: #no prereqs, has geneds
        match = match3
        course['desc'] = match.group(1)
        course['gen_eds'] = match.group(2)

    elif match4: #has prereqs, but not sameas or geneds
        match = match4
        course['desc'] = match.group(1)
        course['prereqs'] = match.group(2)

    else: #no prereqs, sameas, or geneds -- only desc
        course['desc'] = text

def post_process(course):
    #performs misc post processing on courses, including
    #assigning appropriate values for missing keys

    #set notes to empty list
    course['notes'] = []

    #changes dept of Paideia courses to conform with other depts
    if course['dept'] == 'Paideia':
        course['dept'] = 'PAID'

    course['id'] = course['id'].replace('/',', ')

    if 'hours' not in course:
        course['hours'] = 'N/A'

    if 'desc' not in course:
        course['desc'] = 'N/A'

    if 'prereqs' not in course:
        course['prereqs'] = 'N/A'

    #removes '.' from end of 'sameas' if present and makes it so
    #courses are separated by commas instead of 'and'
    if 'same_as' in course:
        if course['same_as'][-1] == '.':
            course['same_as'] = course['same_as'][:-1]
        course['same_as'] = course['same_as'].replace(' and ',', ')
    else:
        course['same_as'] = 'N/A'

    #removes 'Note: ...' geneds that were incorrectly caught by re
    #otherwise removes various geneds, such as 'E', 'S', and 'R'
    if 'gen_eds' in course:
        if 'Note:' in course['gen_eds']:
            course['notes'].append(course['gen_eds'])
            course['gen_eds'] = 'N/A'
        else:
            #fixes '.' typos
            while '.' in course['gen_eds']:
                course['gen_eds'] = course['gen_eds'].replace('.',',')
            course['gen_eds'] = course['gen_eds'].split(', ')

            #remove unknown gen_eds
            gen_eds_to_remove = ['E','R','S','W','Intel','L']
            for gen_ed in gen_eds_to_remove:
                try:
                    course['gen_eds'].remove(gen_ed)
                except ValueError:
                    pass

            #replace misspelled 'Inctl' with 'Intcl'
            try:
                course['gen_eds'].remove('Inctl')
                course['gen_eds'].append('Intcl')
            except:
                pass

            #replace conditional gen_eds with basic ones
            #and add condition to course['notes']
            for gen_ed in course['gen_eds']:
                if len(gen_ed) > 5:
                    new_gen_ed = ""
                    cur_char = gen_ed[0]
                    while cur_char.isupper():
                        new_gen_ed += cur_char
                        cur_char = gen_ed[len(new_gen_ed)]
                    course['notes'].append(gen_ed)
                    course['gen_eds'].remove(gen_ed)
                    course['gen_eds'].append(new_gen_ed)

            if len(course['gen_eds']) == 0:
                course['gen_eds'] = 'N/A'
            else:
                course['gen_eds'] = ', '.join(sorted(course['gen_eds']))

    else: #so 'gen_eds' not in course
        course['gen_eds'] = 'N/A'

    #if no notes, sets to 'N/A', else joins them with newline
    if len(course['notes']) == 0:
        course['notes'] = 'N/A'
    else:
        course['notes'] = '\n'.join(course['notes'])

    return course

def get_course_data():
    '''gets the latest course data from luther catalog,
    which it returns as a list of dictionaries'''

    url_list = create_url_list()
    opener = urllib2.build_opener()

    course_list = []
    cur_course = {}

    for url in url_list:
        request = urllib2.Request(url)
        html_doc = opener.open(request).read()
        html_soup = bs4.BeautifulSoup(html_doc)

        for p in html_soup.find_all('p'):

            if 'coursetitle' in p['class']:
                # append current course to list and set current course equal to empty dict
                # unless current course is already empty, meaning the loop just started
                if cur_course:
                    course_list.append(cur_course)
                    cur_course = {}

                false_course = False
                if p.text == 'Language Learning Center': #special case of a 'false' course
                    false_course = True

                else:
                    parse_coursetitle(p.text.encode('ascii','ignore'), cur_course)

            elif 'credithours' in p['class'] and not false_course:
                parse_credithours(p.text.encode('ascii','ignore'), cur_course)

            elif 'coursedescriptions' in p['class'] and not false_course:
                parse_coursedescriptions(p.text.encode('ascii','ignore'), cur_course)

    course_list.append(cur_course) #append final course

    course_list = [post_process(course) for course in course_list]

    return course_list

def main():
    #test function, gets course data and prints it
    course_data = get_course_data()
    gen_ed_list = []
    for course in course_data:
        for gen_ed in course['gen_eds'].split(', '):
            if gen_ed not in gen_ed_list:
                gen_ed_list.append(gen_ed)
        if course['notes'] != 'N/A':
            print course['notes']
        #print 'id:', course['id']
        #print 'dept:', course['dept']
        #print 'number:', course['number']
        #print 'title:', course['title']
        #print 'hours:', course['hours']
        #print 'desc:', course['desc']
        #print 'prereqs:', course['prereqs']
        #print 'same_as:', course['same_as']
        #print 'gen_eds:', course['gen_eds']
        #print 'notes:', course['notes']
        #print ''
        pass
    print sorted(gen_ed_list)

                        

if __name__ == '__main__':
    main()
