from session_provider import session


def create(obj):
    session.add(obj)
    session.commit()
