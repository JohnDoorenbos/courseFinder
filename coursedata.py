import urllib2, re, bs4

def create_url_list():
    '''Creates the list of urls for each departments course listings'''
    opener = urllib2.build_opener()
    html_doc = opener.open('http://www.luther.edu/catalog/toc.htm').read()
    html_soup = bs4.BeautifulSoup(html_doc)

    url_list = []

    for a in html_soup.find_all('a'):
        if 'Courses' in a.text:
            url_list.append('http://www.luther.edu/catalog/' + a['href'])

    return url_list

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

def postprocess_course(course):
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

def get_course_data(quiet=True):
    '''gets the latest course data from luther catalog,
    which it returns as a list of dictionaries'''

    url_list = create_url_list()
    opener = urllib2.build_opener()

    course_list = []
    cur_course = {}

    for url in url_list:
        if not quiet:
            print "Requesting page " + str(url_list.index(url)+1) + " of " +str(len(url_list))
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

    course_list = [postprocess_course(course) for course in course_list]
    courses_dict = {}
    for course in course_list:
        courses_dict[course['id']] = course

    return courses_dict


#-----------Beginning of Sections data 


def preprocess_sections(section_data):
    processed_data = section_data

    #remove the beginning lines before section data begins
    line_num = 0
    data_started = False
    while not data_started:
        if re.match('^[A-Z]+-\d{3}.?-[\dA-Z]+$',processed_data[line_num][0]):
            data_started = True
        else:
            line_num += 1
    processed_data = processed_data[line_num:]

    #remove lines that do not have section id (talk w/ John about this)
    lines_to_delete = []
    for l in processed_data:
        if l[0] == '':
            lines_to_delete.append(l)
    for l in lines_to_delete:
        processed_data.remove(l)

    #strip white spaces from all data
    for i in range(len(processed_data)):
        for j in range(len(processed_data[i])):
            processed_data[i][j] = processed_data[i][j].strip()
    
    return processed_data

def get_section_data(term):

    #Make sure a valid term was entered
    #and that data is available for the term
    if re.match('\d{4}([Ff][Aa])|([Ss][Pp])',term):
        try:
            term_file_loc = 'sections/'+term.upper()+'.dat'
            term_file = open(term_file_loc,'r')
        except IOError:
            print 'No data available for ' + term + ' sections.'
            return []
    else:
        print 'Terms need the four digit year followed by a two-letter code (ie \'FA\' or \'SP\'). \'' + term + '\' is invalid'
        return []

    file_data = preprocess_sections([l.split('|') for l in term_file.readlines()])
    term_file.close()
    section_data = []

    for l in file_data:
        section = {}
        section['id'] = l[0].replace('-',' ')
        match = re.match('^([A-Z]+)-(\d{3}).?-[\dA-Z]+$',l[0])
        section['course_id'] = match.group(1) + ' ' + match.group(2)
        section['min_credits'] = l[1]
        if l[2] == '':
            section['max_credits'] = l[1]
        else:
            section['max_credits'] = l[2]
        section['title'] = l[3]

        #l[4] is first name of first instructor
        #l[5] is last names of all instructors
        #return as primary_instructor (full name)
        #and other_instructors (last names)
        if l[4] and l[5]:
            last_names = l[5].replace(' ','').split(',')
            section['primary_instructor'] = l[4] + ' ' + last_names[0]
            if len(last_names) > 1:
                section['other_instructors'] = ', '.join(last_names[1:])
            else:
                section['other_instructors'] = 'N/A'
        else:
            section['primary_instructor'] = 'N/A'
            section['other_instructors'] = 'N/A'

        section['building'] = l[6]
        section['room'] = section['building'] + ' ' + l[7]
        if l[8] == '':
            section['start_time'] = 'N/A'
        else:
            section['start_time'] = l[8]
        if l[9] == '':
            section['end_time'] = 'N/A'
        else:
            section['end_time'] = l[9]
        if l[10] == '':
            section['days'] = 'N/A'
        else:
            section['days'] = l[10].replace(' ','')
            if section['days'] == 'TT':
                section['days'] = 'TR'
        if l[11] == '':
            section['seven_weeks'] = 'N/A'
        elif re.match('[Ff]irst',l[11]):
            section['seven_weeks'] = 'first'
        elif re.match('[Ss]econd',l[11]):
            section['seven_weeks'] = 'second'
        section_data.append(section)
    
    sections_dict = {}
    for section in section_data:
        sections_dict[section['id']] = section
    return sections_dict

def get_all_vals(key,term=None):
    '''function for debugging - prints list of all values
    associated with key. Uses section data if term provided,
    else uses course data'''
    if term:
        data = get_section_data(term)
    else:
        data = get_course_data()

    all_vals = []
    for d in data:
        if key in d:
            if d[key] not in all_vals:
                all_vals.append(d[key])

    return sorted(all_vals)
        

def main():
    #test function, gets course data and prints it
    course_data = get_section_data("2014FA")
    for course in course_data:
        print(course)
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

if __name__ == '__main__':
    main()
