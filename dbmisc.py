from dbsearch import Course, AltDesc, GenEd

def get_depts(session):
    res = session.query(Course)

    dept_list = []
    for course in res:
        if course.dept not in dept_list:
            dept_list.append(course.dept)

    return dept_list

def get_alt_desc_ids(session):
    res = session.query(AltDesc)
    alt_desc_id_list = [alt_desc.alt_desc_id for alt_desc in res]
    return alt_desc_id_list

def next_alt_desc_id(session):
    alt_desc_id_list = sorted(get_alt_desc_ids(session))
    if 0 not in alt_desc_id_list:
        return 0
    else:
        for alt_desc_id in alt_desc_id_list:
            new_id = alt_desc_id + 1
            if new_id not in alt_desc_id_list:
                return new_id
