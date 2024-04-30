from flask import render_template, request, redirect, url_for, flash
from dishcovery import app, recipeData, recipeDetails
import requests
import os
from dishcovery.forms import RegisterForm
from dishcovery.models import User
from dishcovery.models import db_storage


@app.route("/login", strict_slashes=False)
def login_route():
    """Serves Login Page"""
    return render_template('login.html')


@app.route("/register", strict_slashes=False, methods=["POST", "GET"])
def register_route():
    """ Serves register page """
    # will deal with form
    form = RegisterForm()
    if form.validate_on_submit():
        user_to_create = User(firstname=form.first_name.data,
                              lastname=form.last_name.data,
                              email=form.email_address.data,
                              password=form.password1.data
                              )
        db_storage.new(user_to_create)
        db_storage.save()
        # redirect the user to the specific route using redirect and url_for
        return redirect(url_for('login_route'))
    if form.errors != {}:
        for err_msg in form.errors.values():
            flash(f'{err_msg}', category="danger")
    return render_template('register.html', form=form)


@app.route("/home", strict_slashes=False)
@app.route("/", strict_slashes=False)
def home_route():
    """ Serves the home page """
    return render_template('home.html')


@app.route("/recipe_finder", strict_slashes=False)
def recipe_finder():
    """ Serves the recipe finder page """
    cuisine_types = ['(Default) - Any', 'American', 'Asian', 'British',
                     'Caribbean', 'Central Europe', 'Chinese',
                     'Eastern Europe', 'French', 'Indian', 'Italian',
                     'Japanese', 'Kosher', 'Mediterranean', 'Mexican',
                     'Middle Eastern', 'Nordic', 'South American',
                     'South East Asian']
    meal_types = ['(Default) - Any', 'Breakfast', 'Dinner', 'Lunch', 'Snack',
                  'Teatime']
    dish_types = ['(Default) - Any', 'Biscuits and cookies', 'Bread',
                  'Cereals', 'Condiments and sauces', 'Desserts', 'Drinks',
                  'Main course', 'Pancake', 'Preps', 'Preserve', 'Salad',
                  'Sandwiches', 'Side dish', 'Soup', 'Starter', 'Sweets']
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
    ingredients = request.get_json()['ingredients']
    cuisineType = request.get_json()['cuisineType']
    mealType = request.get_json()['mealType']
    dishType = request.get_json()['dishType']

    ingredients_list = []
    ingredients = [ingredients_list.append(ing.strip()) for ing in ingredients]
    # sets to empty string if mealType not selected
    ingredients_string = ",".join(ingredients_list)
    # sets to empty string if cuisineType not selected
    cuisine_string = ("&cuisineType=" + cuisineType if cuisineType != "" else
                      "")
    # sets to empty string if mealType not selected
    meal_string = ("&mealType=" + mealType if mealType != "" else "")
    # sets to empty string if dishType not selected
    dish_string = ("&dishType=" + dishType if dishType != "" else "")

    recipe_query = "".join(ingredients_string + cuisine_string + meal_string +
                           dish_string)  # collects the recipe search params

    # print("Recipe Details: ", recipe_query)

    # Keeps the recipeData list to hold only one recipe find query
    # and empties it if new query is made
    if len(recipeData) and recipe_query != "":
        recipeData.pop()
        # recipeDetails = {}
    if recipe_query:
        print(recipe_query)
        recipeData.append(recipe_query)

    print("recipeData: ", recipeData[0])
    return redirect(url_for('result_route', recipe_details=recipe_query))


@app.route("/results", strict_slashes=False)
def result_route():
    """ Shows results for recipe """
    hits = []
    if len(recipeData):
        # calls method to handle api call if request is not present
        recipeDetails = findRecipe(recipeData[0])
        hits = recipeDetails["hits"]

    if hits != []:
        print("Hits found")
    else:
        print("Not Hits found")
    return render_template('results.html', recipe_details=hits)


def findRecipe(recipeParam):
    """Finds recipe and returns response list"""
    try:
        api_key = os.environ.get("API_KEY")
        api_id = os.environ.get("API_ID")
        recipe_query = f"https://api.edamam.com/api/recipes/v2?type=public&app_id={api_id}&app_key={api_key}&q={recipeParam}"
        response = requests.get(recipe_query)
        response.raise_for_status()
    except requests.RequestException:
        return None
    try:
        result = response.json()
        # print(result)
        if len(recipeDetails):
            recipeDetails.pop()
            recipeDetails.append(result)
        return result
    except (KeyError, TypeError, ValueError):
        return None
