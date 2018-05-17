from session_provider import session


def read_all(type):
    data = session.query(type).all()
    # session.close()
    return data


def read_by_id(type, kwargs={}):
    data = session.query(type).filter_by(**kwargs).first()
    # session.close()
    return data


def find_by(type, kwargs={}):
    data = session.query(type).filter_by(**kwargs)
    return data
