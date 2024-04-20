from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://dishcovery_dev:dishcovery_dev_pwd@localhost/dishcovery_dev_db'
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
# with app.app_context():
# 	db.create_all()

from dishcovery import routes
from dishcovery import models
