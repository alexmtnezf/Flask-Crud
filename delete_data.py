from sqlalchemy import inspect

from database_setup import MenuItem
from session_provider import session


def testing():
    veggie_burger = session.query(MenuItem).filter_by(name="Veggie Burger").first()
    session.delete(veggie_burger)
    print(session.deleted)
    session.commit()
    # session.close()
    print(inspect(veggie_burger).detached)


def delete_data(obj):
    session.delete(obj)
    # print(session.deleted)
    session.commit()
    # session.close()
