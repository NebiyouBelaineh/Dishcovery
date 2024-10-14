from flask import render_template, request, redirect, url_for, flash, Response
from dishcovery import app, recipeData, recipeDetails
import requests
import os
from dishcovery.forms import RegisterForm, LoginForm
from dishcovery.models.user import User
from dishcovery.models.bookmark import Bookmark
from dishcovery.models import db_storage
from flask_login import login_user, logout_user, login_required, current_user
import json
import signal
import re


@app.route("/login", strict_slashes=False, methods=['POST', 'GET'])
def login_route():
    """Serves Login Page"""
    form = LoginForm()
    if form.validate_on_submit():
        attempted_user = db_storage.getSession().query(User).filter_by(
            email=form.email_address.data).first()
        if attempted_user and attempted_user.check_password(
                attempted_password=form.password1.data):
            login_user(attempted_user)
            # flash(f'Success! You are logged in as:
            # {attempted_user.full_name()}', category='success')
            return redirect(url_for('recipe_finder'))
        else:
            flash('Username and password are not match! Please try again',
                  category='danger')
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
        flash(f"User {user_to_create.full_name()} created successfully! please\
sign in to access the app", category="info")
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
    return render_template('homepage.html')


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
@login_required
def bookmark_route():
    """ Serves the bookmarks page """
    bookmarks = current_user.bookmarks
    # print("bookmarks", bookmarks)
    if bookmarks != []:
        return render_template('bookmarks.html', bookmark_details=bookmarks)
    else:
        return render_template('bookmarks_not_found.html')


@app.route("/save_bookmark", strict_slashes=False, methods=['POST'])
@login_required
def save_bookmark_route():
    """Saves bookmark if it is not saved alread"""
    bookmark_details = request.get_json()
    label = bookmark_details.get("label")
    source = bookmark_details.get("source")
    image_link = bookmark_details.get("img")
    ingredients = bookmark_details.get("ingredients")
    calories = bookmark_details.get("calories")
    total_time = bookmark_details.get("totalTime")
    link = bookmark_details.get("link")
    tags = bookmark_details.get("tags")

    ingredients_str = json.dumps(ingredients)
    tags_str = json.dumps(tags)

    bookmark_details["ingredients"] = ingredients_str
    bookmark_details["tags"] = tags_str
    bookmark_details["user_id"] = current_user.id

    # bookmark = Bookmark(bookmark_details["user_id"])
    bookmark = Bookmark(
        label=label,
        source=source,
        image_link=image_link,
        ingredients=ingredients_str,
        total_time=total_time,
        calories=calories,
        link=link,
        tags=tags_str,
        user_id=current_user.id
        )
    bookmark.save()
    response = json.dumps({"message": "Bookmark saved."})
    response = Response(
        response=response, status=200, mimetype="application/json")
    return response


@app.route("/get_bookmark", strict_slashes=False, methods=['POST'])
@login_required
def get_bookmark_route():
    """Returns bookmark from DB using its ID"""
    bookmark_id = request.get_json()
    # print(bookmark_id)

    bookmark = db_storage.getSession().query(Bookmark).filter_by(
        id=bookmark_id.get("recipeId")).first()
    bookmarkJSON = json.dumps(bookmark.to_dict())
    print(type(bookmarkJSON))
    response = Response(
        response=bookmarkJSON, status=200, mimetype="application/json")
    return response


@app.route("/get_recipe", strict_slashes=False, methods=['POST'])
def get_recipe_route():
    """Returns recipe from API call using its index"""
    recipe = request.get_json()
    print(recipe)
    recipe_index = int(recipe.get("recipeId"))
    print((recipe_index))
    print(type(recipe_index))

    if recipeDetails != []:
        recipe_hit = recipeDetails[0][recipe_index].get("recipe")
        recipeJSON = json.dumps(recipe_hit)
    else:
        recipeJSON = json.dumps({})
    response = Response(
        response=recipeJSON, status=200, mimetype="application/json")
    return response


@app.route("/check_bookmark", strict_slashes=False, methods=['POST'])
@login_required
def check_bookmark_route():
    """Checks if recipe is bookmarked from DB using its link"""
    bookmark_link = request.get_json().get("link")
    print(bookmark_link, type(bookmark_link))

    bookmark = db_storage.getSession().query(Bookmark).filter_by(
        link=bookmark_link).first()
    # print("bookmark", (bookmark))
    # print("bookmark", type(bookmark))
    if bookmark is None:
        status = {"message": "Not Found"}
    else:
        status = {"message": "Found"}
    bookmark_status = json.dumps(status)
    print("bookmark_status: ", bookmark_status)
    print("bookmark_status type: ", type(bookmark_status))
    response = Response(
        response=bookmark_status, status=200, mimetype="application/json")
    return response


@app.route("/delete_bookmark", strict_slashes=False, methods=['POST'])
@login_required
def delete_bookmark_route():
    """Deletes a bookmark from DB using its ID"""
    bookmark_id = request.get_json()
    # print("bookmark_id" ,bookmark_id)

    bookmark = db_storage.getSession().query(Bookmark).filter_by(
        id=bookmark_id.get("recipeId")).first()
    # print("bookmark obj to delete: ", type(bookmark))
    bookmark.delete()
    db_storage.save()

    response = json.dumps({"message": "Deleted Bookmark."})
    response = Response(
        response=response, status=200, mimetype="application/json")
    return response


@app.route("/settings", strict_slashes=False, methods=["GET", "POST"])
@login_required
def settings_route():
    """ Serves the settings page """
    if request.method == "POST":
        # First name
        name = request.form.get("first_name").strip()
        if name:
            user_to_update = db_storage.getSession().query(User).get(
                current_user.id)
            user_to_update.firstname = name
            db_storage.save()
            flash("First name changed successfully!", category='success')
            return render_template(
                'settings.html',
                message="message1",
                first_name=user_to_update.firstname.capitalize(),
                email_address=user_to_update.email,
                last_name=user_to_update.lastname.capitalize())
        # Last name
        last_name = request.form.get("last_name").strip()
        if last_name:
            user_to_update = db_storage.getSession().query(User).get(
                current_user.id)
            user_to_update.lastname = last_name
            db_storage.save()
            flash("Last name changed successfully!", category='success')
            return render_template(
                'settings.html',
                message="message2",
                first_name=user_to_update.firstname.capitalize(),
                email_address=user_to_update.email,
                last_name=user_to_update.lastname.capitalize())

        # Email Address
        email_address = request.form.get("email_address").strip()
        if email_address:
            user_to_update = db_storage.getSession().query(User).get(
                current_user.id)
            # check if valid email
            if not is_valid_email(email_address):
                flash("Email is not valid!", category='danger')
                return render_template(
                    'settings.html',
                    message="message3",
                    first_name=user_to_update.firstname.capitalize(),
                    email_address=user_to_update.email,
                    last_name=user_to_update.lastname.capitalize())
            # check if email doesnt exist in the database
            if exist_email_address(email_address):
                flash("Email address already exists!\
Please try different email address", category='danger')
                return render_template(
                    'settings.html',
                    message="message3",
                    first_name=user_to_update.firstname.capitalize(),
                    email_address=user_to_update.email,
                    last_name=user_to_update.lastname.capitalize())

            user_to_update.email = email_address
            db_storage.save()
            flash("Email address changed successfully!", category='success')
            return render_template(
                'settings.html',
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
            hashed_new_password = bcrypt.generate_password_hash(
                                                                new_password
                                                                ).decode(
                                                                    'utf-8')
            error_list = []

            # check the length less then
            if (len(new_password) < 6):
                error_list.append("Password length is less then 6 characters!")
            # check the cuurent password is right
            if not current_user.check_password(current_password):
                error_list.append("Current password is wrong!")

            # check the new password and its confirmation is right
            if not bcrypt.check_password_hash(hashed_new_password,
                                              confirmation_password):
                error_list.append(
                    "Password and confirmation password doesn't match")
            if error_list != []:
                for error_message in error_list:
                    flash(f"{error_message}", category='danger')
                return render_template(
                    'settings.html',
                    message="message4",
                    first_name=current_user.firstname.capitalize(),
                    email_address=current_user.email,
                    last_name=current_user.lastname.capitalize())

            current_user.password = new_password
            db_storage.save()
            flash("Password changed successfully!", category='success')
            return render_template(
                'settings.html',
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

    # Keeps the recipeData list to hold only one recipe find query
    # and empties it if new query is made
    if len(recipeData) and recipe_query != "":
        recipeData.pop()

    if recipe_query:
        # print(recipe_query)
        recipeData.append(recipe_query)

    # print("recipeData: ", recipeData[0])
    return redirect(url_for('result_route'))


@app.route("/results", strict_slashes=False)
def result_route():
    """ Shows results for recipe """
    hits = []
    if len(recipeData):
        # calls method to handle api call if request is not present
        recipe_details = findRecipe(recipeData[0])
        if recipe_details:  # check if recipe_details is not None
            hits = recipe_details["hits"]
            writeResponse(recipe_details)  # Writes response to a JSON file
            recipeDetails.clear()
            recipeDetails.append(hits)
        else:
            print("Request returned NULL")

    if hits != []:
        print("Hits found")
        return render_template('results.html', recipe_details=hits)
    else:  # Serves recipe_not_found page if no hits found with redirect option
        print("Not Hits found")
        return render_template('recipe_not_found.html')
# -------------------------- NON Route methods --------------------------


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
        return result
    except (KeyError, TypeError, ValueError):
        return None


def writeResponse(response):
    """Write the response from the api call to a JSON file"""
    file_path = 'dishcovery/static/data/tmp/response.json'

    try:
        with open(file_path, 'w') as file:
            file.write((json.dumps(response)))
            print("JSON object saved to", file_path)
    except FileNotFoundError:
        pass


def delete_file():
    """Delete the file"""
    # Define the path of the file to be removed
    file_path = 'dishcovery/static/data/tmp/response.json'
    # Check if the file exists before trying to remove it
    if os.path.exists(file_path):
        os.remove(file_path)
        print(f"File {file_path} removed.")


def signal_handler(signum, frame):
    """Signal hanler"""
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
    """Check if the email address exists"""
    user = db_storage.getSession().query(User).filter_by(
                                                        email=email_to_check
                                                        ).first()
    if user:
        return True
    else:
        return False
