from flask import render_template, request, redirect, url_for, flash
from dishcovery import app, recipeData, recipeDetails
import requests
import os
from dishcovery.forms import RegisterForm, LoginForm
from dishcovery.models import User
from dishcovery.models import db_storage
from flask_login import login_user, logout_user, login_required, current_user
import json
import signal
import re

@app.route("/login", strict_slashes=False, methods=['POST','GET'])
def login_route():
    """Serves Login Page"""
    form = LoginForm()
    if form.validate_on_submit():
        attempted_user = db_storage.getSession().query(User).filter_by(email=form.email_address.data).first()
        if attempted_user and attempted_user.check_password(
            attempted_password=form.password1.data):
            login_user(attempted_user)
            # flash(f'Success! You are logged in as: {attempted_user.full_name()}', category='success')
            return redirect(url_for('recipe_finder'))
        else:
            flash('Username and password are not match! Please try again', category='danger')
    if form.errors != {}:
        print(form.errors)
        for err_msg in form.errors.values():
            flash(f'{err_msg}', category="danger")
        
    return render_template('login.html', form=form)


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
        flash(f"User {user_to_create.full_name()} created successfully! please sign in to access the app", category="info")
        # redirect the user to the specific route using redirect and url_for
        return redirect(url_for('login_route'))
    if form.errors != {}:
        print(form.errors)
        for err_msg in form.errors.values():
            flash(f'{err_msg}', category="danger")
    return render_template('register.html', form=form)


@app.route("/home", strict_slashes=False)
@app.route("/", strict_slashes=False)
def home_route():
    """ Serves the home page """
    return render_template('home.html')


@app.route("/recipe_finder", strict_slashes=False)
@login_required
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
@login_required
def bookmark_route():
    """ Serves the bookmarks page """
    return render_template('bookmarks.html')


@app.route("/settings", strict_slashes=False, methods=["GET","POST"])
@login_required
def settings_route():
    """ Serves the settings page """
    if request.method == "POST":
        # First name
        name = request.form.get("first_name").strip()
        if name:
            user_to_update = db_storage.getSession().query(User).get(current_user.id)
            user_to_update.firstname = name
            db_storage.save()
            flash("First name changed successfully!", category='success')
            return render_template('settings.html',
                           message="message1",
                           first_name=user_to_update.firstname.capitalize(),
                           email_address=user_to_update.email,
                           last_name=user_to_update.lastname.capitalize())
        #Last name
        last_name = request.form.get("last_name").strip()
        if last_name:
            user_to_update = db_storage.getSession().query(User).get(current_user.id)
            user_to_update.lastname = last_name
            db_storage.save()
            flash("Last name changed successfully!", category='success')
            return render_template('settings.html',
                           message="message2",
                           first_name=user_to_update.firstname.capitalize(),
                           email_address=user_to_update.email,
                           last_name=user_to_update.lastname.capitalize())
        #Email Address
        email_address = request.form.get("email_address").strip()
        if email_address:
            user_to_update = db_storage.getSession().query(User).get(current_user.id)
            # check if valid email
            if not is_valid_email(email_address):
                flash("Email is not valid!", category='danger')
                return render_template('settings.html',
                           message="message3",
                           first_name=user_to_update.firstname.capitalize(),
                           email_address=user_to_update.email,
                           last_name=user_to_update.lastname.capitalize())
            # check if email doesnt exist in the database
            if exist_email_address(email_address):
                flash("Email address already exists! Please try different email address", category='danger')
                return render_template('settings.html',
                           message="message3",
                           first_name=user_to_update.firstname.capitalize(),
                           email_address=user_to_update.email,
                           last_name=user_to_update.lastname.capitalize())
                
            user_to_update.email = email_address
            db_storage.save()
            flash("Email address changed successfully!", category='success')
            return render_template('settings.html',
                           message="message3",
                           first_name=user_to_update.firstname.capitalize(),
                           email_address=user_to_update.email,
                           last_name=user_to_update.lastname.capitalize())
        # password
        current_password = request.form.get("current_pass").strip()
        new_password = request.form.get("new_pass").strip()
        confirmation_password = request.form.get("confirm_pass").strip()
        if current_password and new_password and confirmation_password:
            from dishcovery import bcrypt
            hashed_new_password = bcrypt.generate_password_hash(new_password).decode('utf-8')
            error_list = []
            #check the length less then
            if(len(new_password) < 6):
                error_list.append("Password length is less then 6 characters!")
            #check the cuurent password is right
            if not current_user.check_password(current_password):
                error_list.append("Current password is wrong!")
            
            #check the new password and its confirmation is right
            if not bcrypt.check_password_hash(hashed_new_password, confirmation_password):
                error_list.append("Password and confirmation password doesn't match")
            if error_list != []:
                for error_message in error_list:
                    flash(f"{error_message}", category='danger')
                return render_template('settings.html',
                           message="message4",
                           first_name=current_user.firstname.capitalize(),
                           email_address=current_user.email,
                           last_name=current_user.lastname.capitalize())
                
            current_user.password = new_password
            db_storage.save()
            flash("Email address changed successfully!", category='success')
            return render_template('settings.html',
                           message="message4",
                           first_name=current_user.firstname.capitalize(),
                           email_address=current_user.email,
                           last_name=current_user.lastname.capitalize())
            
    return render_template('settings.html',
                           message="message1",
                           first_name=current_user.firstname.capitalize(),
                           email_address=current_user.email,
                           last_name=current_user.lastname.capitalize())


@app.route("/logout", strict_slashes=False)
@login_required
def logout_route():
    """ Logs out user and serves login page """
    logout_user()
    flash('You have been logged out Successfully!', category="info")
    return redirect(url_for('login_route'))


@app.route("/search", strict_slashes=False, methods=['POST'])
@login_required
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
@login_required
def result_route():
    """ Shows results for recipe """
    hits = []
    if len(recipeData):
        # calls method to handle api call if request is not present
        recipeDetails = findRecipe(recipeData[0])
        if recipeDetails:  # check if recipeDetails is not None
            hits = recipeDetails["hits"]
            writeResponse(recipeDetails)  # Writes response to a JSON file
        else:
            print("Request returned NULL")

    if hits != []:
        print("Hits found")
        return render_template('results.html', recipe_details=hits)
    else:  # Serves recipe_not_found page if no hits found with redirect option
        print("Not Hits found")
        return render_template('recipe_not_found.html')


def findRecipe(recipeParam):
    """Finds recipe and returns response list"""
    try:
        api_key = os.environ.get("API_KEY")
        api_id = os.environ.get("API_ID")
        recipe_query = f"https://api.edamam.com/api/recipes/v2?type=public&\
app_id={api_id}&app_key={api_key}&q={recipeParam}"
        response = requests.get(recipe_query)
        response.raise_for_status()
    except requests.RequestException as e:
        print(e)
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


def writeResponse(response):
    """Write the response from the api call to a JSON file"""
    file_path = 'dishcovery/static/data/tmp/response.json'

    with open(file_path, 'w') as file:
        file.write((json.dumps(response)))

    print("JSON object saved to", file_path)


def delete_file():
    # Define the path of the file to be removed
    file_path = 'dishcovery/static/data/tmp/response.json'
    # Check if the file exists before trying to remove it
    if os.path.exists(file_path):
        os.remove(file_path)
        print(f"File {file_path} removed.")


def signal_handler(signum, frame):
    # Call delete_file function before exiting
    try:
        delete_file()
    except Exception:
        pass
    # Exit program
    exit()


# Register signal handler for SIGINT (Ctrl+C)
signal.signal(signal.SIGINT, signal_handler)


# check valid email
def is_valid_email(email):
    """
    Check if a string is a valid email address.
    
    Args:
        email (str): The string to be checked.
    
    Returns:
        bool: True if the email is valid, False otherwise.
    """
    # Regular expression pattern for validating email addresses
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    
    # Use re.match to search the pattern at the beginning of the string
    if re.match(pattern, email):
        return True
    else:
        return False

def exist_email_address(email_to_check):
        user = db_storage.getSession().query(User).filter_by(email=email_to_check).first()
        if user:
            return True
        else:
            return False
