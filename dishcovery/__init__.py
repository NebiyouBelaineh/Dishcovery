from flask import Flask
from dishcovery.models import db_storage

db_storage.reload()

app = Flask(__name__)

# an empty list to hold recipe find queries
recipeData = []
# an empty list to hold recipe api response
recipeDetails = []

from dishcovery import routes
from dishcovery import models
