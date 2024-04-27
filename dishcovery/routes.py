from flask import render_template, request, redirect, url_for
from  dishcovery import app
from dishcovery import recipeData
import requests
import os


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
    cuisine_types = ['(Default) - Any', 'American', 'Asian', 'British', 'Caribbean', \
        'Central Europe', 'Chinese', 'Eastern Europe', 'French',\
            'Indian', 'Italian', 'Japanese' ,'Kosher', 'Mediterranean',\
                'Mexican', 'Middle Eastern', 'Nordic', 'South American',\
                    'South East Asian']
    meal_types = ['(Default) - Any', 'Breakfast', 'Dinner', 'Lunch', 'Snack', 'Teatime']
    dish_types = ['(Default) - Any', 'Biscuits and cookies', 'Bread', 'Cereals',\
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



@app.route("/search", strict_slashes=False, methods=['POST'])
def search_route():
    """ Search for recipe """
    recipe_details = request.get_json()
    if len(recipeData):
        recipeData.pop()
    if recipe_details:
        print(recipe_details);
        recipeData.append(recipe_details)
    return redirect(url_for('result_route', recipe_details=recipe_details))


@app.route("/results", strict_slashes=False)
def result_route():
    """ Shows results for recipe """
    # recipe_details = recipeData
    recipe_details = findRecipe(recipeData)
    print('Inside result_route')
    print('recipe_details: ',recipe_details)
    return render_template('results.html', recipe_details=recipe_details)

def findRecipe(recipeParam):
    """Finds recipe and returns response list"""
    try:
        api_key = os.environ.get("API_KEY")
        api_id = os.environ.get("API_ID")
        response = requests.get(
            f"https://api.edamam.com/api/recipes/v2?type=public&app_id={api_id}&app_key={api_key}&q={recipeParam}")
        response.raise_for_status()
    except requests.RequestException:
        return None
    try:
        result = response.json()
        print(result)
        return result
    except (KeyError, TypeError, ValueError):
        return None
