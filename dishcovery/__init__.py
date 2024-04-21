from flask import Flask
from dishcovery.models import db_storage

db_storage.reload()

app = Flask(__name__)

# print("*****************inside models********************")
from dishcovery import routes
from dishcovery import models
