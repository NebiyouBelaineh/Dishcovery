from flask import Flask
from dishcovery.models import db_storage
from os import environ
from dotenv import load_dotenv
from flask_bcrypt import Bcrypt

load_dotenv()
db_storage.reload()

app = Flask(__name__)
# is a security shield for displaying the form
app.config["SECRET_KEY"]=environ.get("DISHCOVERY_SECRET_KEY")
# an empty list to hold recipe find queries
recipeData = []
# an empty list to hold recipe api response
recipeDetails = []
bcrypt = Bcrypt(app)

from dishcovery import routes
from dishcovery import models
