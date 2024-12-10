from flask import Flask, request, jsonify, make_response, Response 
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
from api_client import CalorieNinjasAPIClient  # Change from 'get_nutrition' to the class
import os

# Load environment variables from .env file
load_dotenv()

# Access the API key
API_KEY = os.getenv('API_KEY')

# Initialize the API client
api_client = CalorieNinjasAPIClient(api_key=API_KEY)

# Initialize the Flask app
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///calorie_tracker.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize the database
db = SQLAlchemy(app)

# Create the database tables
with app.app_context():
    db.create_all()

