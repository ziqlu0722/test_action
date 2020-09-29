from flask import Flask, request, current_app
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_migrate import Migrate
from config import Config
from flask_httpauth import HTTPBasicAuth

#create instances for various elements
db = SQLAlchemy()
migrate = Migrate()
bcrypt = Bcrypt()
auth = HTTPBasicAuth()

def create_app(config_class=Config):
    #create application with configuration
    app = Flask(__name__)
    app.config.from_object(config_class)

    #initiate various elements
    db.init_app(app)
    migrate.init_app(app, db)
    bcrypt.init_app(app)

    #register blue-print
    from app.user import user_bp
    app.register_blueprint(user_bp, url_prefix='/v1')

    return app

from app import models
