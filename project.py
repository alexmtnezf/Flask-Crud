from flask import Flask
from flask import render_template, request, redirect, url_for, flash, jsonify
from sqlalchemy.orm.exc import NoResultFound, MultipleResultsFound

import read_data
from database_setup import Restaurant, MenuItem

app = Flask(__name__)


# ADD JSON RESTFUL API ENDPOINT HERE
@app.route('/restaurants/JSON')
def restaurants_json():
    rests = read_data.read_all(Restaurant)

    return jsonify(Restaurants=[i.serialize for i in rests])


@app.route('/restaurant/<int:restaurant_id>/menu/JSON')
def restaurant_menu_json(restaurant_id):
    restaurant, items = get_restaurant_menu(restaurant_id)
    return jsonify(MenuItems=[i.serialize for i in items])


@app.route('/restaurant/<int:restaurant_id>/menu/<int:menu_id>/JSON')
def restaurant_menu_item_json(restaurant_id, menu_id):
    try:
        restaurant = read_data.read_by_id(Restaurant, {'id': restaurant_id})
        kwargs = {'restaurant_id': restaurant.id, 'id': menu_id}
        item = read_data.find_by(MenuItem, kwargs).one()
    except NoResultFound:
        raise Exception("Not found")
    except MultipleResultsFound as ex:
        return "He likes study too much---"
    else:
        return jsonify(MenuItem=item.serialize)


# Non Restful requests

@app.route('/')
@app.route('/restaurants/')
def restaurants():
    rests = read_data.read_all(Restaurant)

    return render_template("restaurants.html", restaurants=rests)


@app.route("/restaurant/<int:restaurant_id>")
@app.route("/restaurant/<int:restaurant_id>/menu")
def restaurant_menu(restaurant_id):
    '''
    Function that returns the menu items for a restaurant
    :param int restaurant_id: Identifier for restaurant
    :return: string the web server response
    '''
    try:
        restaurant, items = get_restaurant_menu(restaurant_id)
    except NoResultFound:
        raise Exception("Not found")
    else:
        return render_template("menu.html", restaurant=restaurant, items=items)


# Task 1: Create route for newMenuItem function here

@app.route('/restaurant/<int:restaurant_id>/menu/new', methods=['GET', 'POST'])
def new_menu_item(restaurant_id):
    if request.method == 'POST':
        mi = MenuItem(name=request.form.get('name'), price=request.form.get('price'),
                      description=request.form.get('description'), course=request.form.get('course'),
                      restaurant_id=restaurant_id)
        import create_data
        create_data.create(mi)
        flash("Menu Item Created!")
        return redirect(url_for('restaurant_menu', restaurant_id=restaurant_id))
    else:
        return render_template('newmenuitem.html', restaurant_id=restaurant_id)


# Task 2: Create route for editMenuItem function here
@app.route('/restaurant/<int:restaurant_id>/menu/<int:menu_id>/edit', methods=['GET', 'POST'])
def edit_menu_item(restaurant_id, menu_id):
    import update_data
    try:
        mi_item = read_data.read_by_id(MenuItem, {'id': menu_id})

    except NoResultFound:
        raise Exception('Not found')

    if request.method == 'POST':

        update_data.update_data(mi_item, name=request.form.get('name'), price=request.form.get('price'),
                                description=request.form.get('description'), course=request.form.get('course'))
        flash("Menu Item Successfully Edited!")
        return redirect(url_for('restaurant_menu', restaurant_id=restaurant_id))
    else:

        return render_template('editmenuitem.html', restaurant_id=restaurant_id, menu=mi_item)


# Task 3: Create a route for deleteMenuItem function here
@app.route('/restaurant/<int:restaurant_id>/menu/<int:menu_id>/delete', methods=['GET', 'POST'])
def delete_menu_item(restaurant_id, menu_id):
    try:
        item_delete = read_data.read_by_id(MenuItem, {'id': menu_id})
    except NoResultFound:
        raise Exception('Not found')
    else:
        if request.method != 'POST':
            return render_template('deletemenuitem.html', item=item_delete)
        else:
            import delete_data
            delete_data.delete_data(item_delete)
            flash("Menu Item Successfully Deleted!")
            return redirect(url_for('restaurant_menu', restaurant_id=restaurant_id))


# Task 4: Create rout for new_restaurant function
@app.route('/restaurant/new', methods=['GET', 'POST'])
def new_restaurant():
    if request.method == 'POST':
        import create_data
        newrest = Restaurant(name=request.form.get('name'))
        create_data.create(newrest)
        flash('New Restaurant Created')
        return redirect(url_for('restaurants'))
    else:
        return render_template('newrestaurant.html')


# Task 5: Create route for edit_restaurant function
@app.route('/restaurant/<int:restaurant_id>/edit', methods=['GET', 'POST'])
def edit_restaurant(restaurant_id):
    try:
        restaurant = read_data.read_by_id(Restaurant, {'id': restaurant_id})

    except NoResultFound:
        raise Exception('Not found')

    if request.method == 'POST':
        import update_data
        update_data.update_data(restaurant, name=request.form.get('name'))
        flash("Restaurant Successfully Edited!")
        return redirect(url_for('restaurants'))
    else:
        return render_template('editrestaurant.html', restaurant=restaurant)


# Task 6: Create route for delete_restaurant function
@app.route('/restaurant/<int:restaurant_id>/delete', methods=['GET', 'POST'])
def delete_restaurant(restaurant_id):
    try:
        restaurant = read_data.read_by_id(Restaurant, {'id': restaurant_id})
    except NoResultFound:
        raise Exception('Not found')
    else:
        if request.method != 'POST':
            return render_template('deleterestaurant.html', restaurant=restaurant)
        else:
            import delete_data
            flash("Restaurant Successfully Deleted!".format(name=restaurant.name))
            delete_data.delete_data(restaurant)
            return redirect(url_for('restaurants'))


def get_restaurant_menu(restaurant_id):
    restaurant = read_data.read_by_id(Restaurant, {'id': restaurant_id})
    kwargs = {'restaurant_id': restaurant.id}
    items = read_data.find_by(MenuItem, kwargs)
    return restaurant, items


if __name__ == '__main__':
    app.debug = True
    app.secret_key = "super_secret_key"
    app.run(host='0.0.0.0', port=5000)
