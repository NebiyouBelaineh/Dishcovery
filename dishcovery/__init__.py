from flask import Flask
from dishcovery.models import storage

app = Flask(__name__)



from dishcovery import routes
from dishcovery import models
