from config import *
from flask import request

class History:
    def __init__(self):
        cookie = request.cookies.get('history')
        if cookie == None:
            self.history = []
        else:
            self.history = eval(cookie)

    def add(self,course):
        course_dict = {'id':course.id, 'title':course.title, 'dept':course.dept}
        if course_dict in self.history:
            self.history.remove(course_dict)
            self.history.insert(0,course_dict)
        else:
            self.history.insert(0,course_dict)
            if len(self.history) > 10: #keep history limited to last 10
                self.history = self.history[:-1]

    def __str__(self):
        return str(self.history)

    def __iter__(self):
        return iter(self.history)
