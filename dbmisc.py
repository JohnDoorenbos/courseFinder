from dbsearch import CourseDB, ReviewDB

def get_depts(session):
    res = session.query(CourseDB)

    dept_list = []
    for course in res:
        if course.dept not in dept_list:
            dept_list.append(course.dept)

    return dept_list

def get_review_ids(session):
    res = session.query(ReviewDB)
    review_id_list = [review.review_id for review in res]
    return review_id_list

def next_review_id(session):
    review_id_list = sorted(get_review_ids(session))
    if 0 not in review_id_list:
        return 0
    else:
        for review_id in review_id_list:
            new_id = review_id + 1
            if new_id not in review_id_list:
                return new_id
