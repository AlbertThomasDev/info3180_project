from flask import Flask
from .config import Config
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_wtf.csrf import CSRFProtect

app = Flask(__name__)
csrf = CSRFProtect(app)
app.config.from_object(Config)

db = SQLAlchemy(app)
login_manager = LoginManager()

migrate = Migrate(app, db)


login_manager.init_app(app)
login_manager.login_view = 'login'

from app import views, models