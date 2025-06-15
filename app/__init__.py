import os
from flask import Flask
from dotenv import load_dotenv
from flask_login import LoginManager
from . import model
from flask_migrate import Migrate

def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)
    load_dotenv()

    print(os.environ)

    app.config.from_prefixed_env()

    # Initialize database
    model.db.init_app(app)
    migrate = Migrate(app, model.db)

    # Initialize login manager
    login_manager = LoginManager()
    login_manager.init_app(app)
    
    
    return app