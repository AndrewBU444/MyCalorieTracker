from flask import Flask
from my_calorie_tracker.db import db
from my_calorie_tracker.routes import auth_bp

def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)
    
    # Register the blueprint for authentication routes
    app.register_blueprint(auth_bp, url_prefix='/auth')

    return app
