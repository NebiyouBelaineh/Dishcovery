from flask import Flask

from os import environ
from dotenv import load_dotenv
from flask_bcrypt import Bcrypt
from flask_login import LoginManager

load_dotenv()
"""
enable this after creating tables;
"""
# from dishcovery.models import db_storage
# db_storage.reload()

app = Flask(__name__)
# is a security shield for displaying the form
app.config["SECRET_KEY"]=environ.get("DISHCOVERY_SECRET_KEY")
# an empty list to hold recipe find queries
recipeData = []
# an empty list to hold recipe api response
recipeDetails = []
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = "login_route"
login_manager.login_message_category = "info"

from dishcovery import routes
from dishcovery import models
