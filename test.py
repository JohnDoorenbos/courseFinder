import urllib2
import bs4
import sqlalchemy

course_ids = list(range(3890,3941)) + [4215,4229]
url_list = ['http://www.luther.edu/catalog/' + str(course_id) + '.htm' for course_id in course_ids]

request = urllib2.Request(url_list[0])
opener = urllib2.build_opener()
html_doc = opener.open(request).read()
soup = bs4.BeautifulSoup(html_doc)
print(soup.prettify())

for p in soup.find_all('p', class_='coursedescriptions'):
    print("")
    print(p.text)

