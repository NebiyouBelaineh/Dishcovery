from flask import render_template
from  dishcovery import app

@app.route("/login", strict_slashes=False)
def login_route():
    """Serves Login Page"""
    return render_template('login.html')


@app.route("/register", strict_slashes=False)
def register_route():
    """ Serves register page """
    return render_template('register.html')


@app.route("/home", strict_slashes=False)
@app.route("/", strict_slashes=False)
def home_route():
    """ Serves the home page """
    return render_template('home.html')

@app.route("/recipe_finder", strict_slashes=False)
def recipe_finder():
    """ Serves the recipe finder page """
    cuisine_types = ['Select Cuisine', 'American', 'Asian', 'British', 'Caribbean', \
        'Central Europe', 'Chinese', 'Eastern Europe', 'French',\
            'Indian', 'Italian', 'Japanese' ,'Kosher', 'Mediterranean',\
                'Mexican', 'Middle Eastern', 'Nordic', 'South American',\
                    'South East Asian']
    meal_types = ['Select Meal', 'Breakfast', 'Dinner', 'Lunch', 'Snack', 'Teatime']
    dish_types = ['Select Dish', 'Biscuits and cookies', 'Bread', 'Cereals',\
        'Condiments and sauces', 'Desserts', 'Drinks', 'Main course',\
            'Pancake', 'Preps', 'Preserve', 'Salad', 'Sandwiches',\
                'Side dish', 'Soup', 'Starter', 'Sweets']
    return render_template('recipe_finder.html', cuisines=cuisine_types,
                           meals=meal_types, dishes=dish_types)


@app.route("/bookmarks", strict_slashes=False)
def bookmark_route():
    """ Serves the bookmarks page """
    return render_template('bookmarks.html')


@app.route("/settings", strict_slashes=False)
def settings_route():
    """ Serves the settings page """
    return render_template('settings.html')


@app.route("/logout", strict_slashes=False)
def logout_route():
    """ Logs out user and serves login page """
    return render_template('login.html')
