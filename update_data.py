from database_setup import Restaurant, MenuItem
from session_provider import session


def testing_update():
    veggieBurger = session.query(MenuItem).filter_by(name='Veggie Burger').first()
    veggieBurger.price = "$5.66"

    print(session.dirty)

    veggieBurgers = session.query(MenuItem).filter_by(name='Veggie Burger')
    for item in veggieBurgers:

        if item.price != "$5.66":
            item.price = "$5.66"

    print()
    # Printing objects already persistent in database but their data was modified in the current session
    print(session.dirty)
    print()

    # Creating a fake restaurant
    fake_restaurant = Restaurant(name="fakerestaurant")
    session.add(fake_restaurant)
    # Checking our new items in the session
    print(session.new)

    # Rollback all changes, so that none change is going to be persisted
    session.rollback()
    print()
    print(veggieBurger.price)
    print(fake_restaurant in session)

    rests = session.query(Restaurant).filter(Restaurant.name.in_(['Pizza Palace', 'fakerestaurant'])).all()
    print(rests)
    print()

    # Now we only wnat to update the first veggieBurger in our session
    veggieBurger.price = "$5.66"
    session.commit()
    print(veggieBurger.price)


def update_data(obj, **kwargs):
    for k, v in kwargs.items():
        setattr(obj, k, v)
    session.commit()
