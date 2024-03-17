from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from config import Config
from flask_migrate import Migrate


emp_app = Flask(__name__)
emp_app.config.from_object(Config)
db = SQLAlchemy(emp_app)
migrate = Migrate(emp_app, db)
login_manager = LoginManager(emp_app)

from emp_app import models
from emp_app import views
