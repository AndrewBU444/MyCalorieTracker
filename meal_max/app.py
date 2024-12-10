from flask import Flask, request, jsonify, make_response, Response 
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from dotenv import load_dotenv
from config import ProductionConfig
from api_client import CalorieNinjasAPIClient  # Change from 'get_nutrition' to the class
import os
from calorie_tracker_model import CalorieTrackerModel
from db import CalorieIntake, WeightLog, db
from werkzeug.security import generate_password_hash, check_password_hash
from meal_max.utils.sql_utils import check_database_connection, check_table_exists

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

#Health Checks
@app.route('/api/health', methods=['GET'])
def healthcheck() -> Response:
    """
    Health check route to verify the service is running.

    Returns:
        JSON response indicating the health status of the service.
    """
    app.logger.info('Health check')
    return make_response(jsonify({'status': 'healthy'}), 200)

@app.route('/api/db-check', methods=['GET'])
def db_check() -> Response:
    """
    Route to check if the database connection and meals table are functional.

    Returns:
        JSON response indicating the database health status.
    Raises:
        404 error if there is an issue with the database.
    """
    try:
        app.logger.info("Checking database connection...")
        check_database_connection()
        app.logger.info("Database connection is OK.")
        app.logger.info("Checking if meals table exists...")
        check_table_exists("meals")
        app.logger.info("meals table exists.")
        return make_response(jsonify({'database_status': 'healthy'}), 200)
    except Exception as e:
        return make_response(jsonify({'error': str(e)}), 404)


# User model with password hashing and salt
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    calorie_goal = db.Column(db.Integer, nullable=False)
    starting_weight = db.Column(db.Integer, nullable=False)
    salt = db.Column(db.String(128), nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)

    def __init__(self, username, password, calorie_goal, starting_weight):
        self.username = username
        self.salt = self.generate_salt()
        self.password_hash = self.generate_password_hash(password)
        self.calorie_goal = calorie_goal
        self.starting_weight = starting_weight

    def generate_salt(self):
        """Generate a random salt"""
        return os.urandom(16).hex()

    def generate_password_hash(self, password):
        """Generate password hash using salt"""
        return generate_password_hash(password + self.salt)

    def check_password(self, password):
        """Check if the provided password matches the stored hash"""
        return check_password_hash(self.password_hash, password + self.salt)

# Calorie Intake model
class CalorieIntake(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    date = db.Column(db.Date, nullable=False)
    calories = db.Column(db.Integer, nullable=False)


# Routes
# 1. Register a user and set a calorie goal (Create Account)
@app.route('/create-account', methods=['POST'])
def create_account():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    calorie_goal = data.get('calorie_goal')
    starting_weight = data.get('starting_weight')

    if not username or not password or not calorie_goal or not starting_weight:
        return jsonify({'error': 'All fields are required'}), 400

    try:
        user = CalorieTrackerModel(
            username=username,
            password=password,
            calorie_goal=calorie_goal,
            starting_weight=starting_weight
        )
        db.session.add(user)
        db.session.commit()
        return jsonify({'message': 'Account created successfully'}), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 400

# 2. Login (Authenticate User)
@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return jsonify({'error': 'Username and password are required'}), 400

    user = User.query.filter_by(username=username).first()
    if not user:
        return jsonify({'error': 'User not found'}), 404

    # Check if the password matches the hashed password
    if not check_password_hash(user.password, password):
        return jsonify({'error': 'Invalid password'}), 401

    return jsonify({'message': 'Login successful'}), 200

# 3. Update password
@app.route('/update-password', methods=['PUT'])
def update_password():
    data = request.get_json()
    username = data.get('username')
    current_password = data.get('current_password')
    new_password = data.get('new_password')

    if not username or not current_password or not new_password:
        return jsonify({'error': 'Username, current password, and new password are required'}), 400

    user = User.query.filter_by(username=username).first()
    if not user:
        return jsonify({'error': 'User not found'}), 404

    # Check if the current password matches
    if not check_password_hash(user.password, current_password):
        return jsonify({'error': 'Incorrect current password'}), 401

    # Hash the new password and update
    user.password = generate_password_hash(new_password)
    db.session.commit()
    return jsonify({'message': 'Password updated successfully'}), 200

# 4. Add daily calorie intake
@app.route('/intake', methods=['POST'])
def add_calorie_intake():
    data = request.get_json()
    username = data.get('username')
    date_str = data.get('date')
    calories = data.get('calories')

    if not username or not date_str or not calories:
        return jsonify({'error': 'Username, date, and calories are required'}), 400

    user = User.query.filter_by(username=username).first()
    if not user:
        return jsonify({'error': 'User not found'}), 404

    try:
        date = datetime.strptime(date_str, '%Y-%m-%d').date()
    except ValueError:
        return jsonify({'error': 'Invalid date format. Use YYYY-MM-DD'}), 400

    intake = CalorieIntake(user_id=user.id, date=date, calories=calories)
    db.session.add(intake)
    db.session.commit()
    return jsonify({'message': 'Calorie intake added successfully'}), 201

@app.route('/intake', methods=['POST'])
def log_calorie_intake():
    data = request.get_json()
    username = data.get('username')
    calories = data.get('calories')
    date_str = data.get('date', None)

    if not username or not calories:
        return jsonify({'error': 'Username and calories are required'}), 400

    try:
        user = CalorieTrackerModel.query.filter_by(username=username).first()
        if not user:
            return jsonify({'error': 'User not found'}), 404

        log_date = datetime.strptime(date_str, '%Y-%m-%d').date() if date_str else datetime.today().date()
        user.log_calories(user_id=user.id, calories=calories, log_date=log_date)
        return jsonify({'message': 'Calorie intake logged successfully'}), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 400

# 5. Get calorie intake history
@app.route('/history/<username>', methods=['GET'])
def get_user_history(username):
    try:
        user = CalorieTrackerModel.query.filter_by(username=username).first()
        if not user:
            return jsonify({'error': 'User not found'}), 404

        summary = user.get_user_summary(username)
        return jsonify(summary), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 400

# 7. Update calorie goal
@app.route('/goal', methods=['PUT'])
def update_goal():
    data = request.get_json()
    username = data.get('username')
    new_goal = data.get('calorie_goal')

    if not username or not new_goal:
        return jsonify({'error': 'Username and new calorie goal are required'}), 400

    user = User.query.filter_by(username=username).first()
    if not user:
        return jsonify({'error': 'User not found'}), 404

    user.calorie_goal = new_goal
    db.session.commit()
    return jsonify({'message': 'Calorie goal updated successfully'}), 200

# 8. Delete user 
@app.route('/delete/<username>', methods=['DELETE'])
def delete_user(username):
    user = User.query.filter_by(username=username).first()
    if not user:
        return jsonify({'error': 'User not found'}), 404

    CalorieIntake.query.filter_by(user_id=user.id).delete()
    db.session.delete(user)
    db.session.commit()
    return jsonify({'message': 'User deleted successfully'}), 200

#===================================================
# Nutrition Routes
#===================================================

@app.route('/nutrition/<food>', methods=['GET'])
def get_nutrition_route(food):
    """
    Route to get full nutrition information for a food item.
    """
    data = api_client.get_nutrition(food)  # Use the api_client instance

    if "items" not in data:
        return jsonify({"error": "No data found"}), 404
    
    nutrition_data = [
        {
            "name": item["name"],
            "calories": item["calories"],
            "protein": item["protein_g"],
            "carbohydrates": item["carbohydrates_total_g"],
            "sugar": item["sugar_g"]
        } for item in data["items"]
    ]
    return jsonify(nutrition_data)

@app.route('/calories/<food>', methods=['GET'])
def get_calories(food):
    """
    Route to get calorie information for a food item.
    """
    data = api_client.get_nutrition(food)
    if "items" not in data:
        return jsonify({"error": "No data found"}), 404
    
    calories_data = [{"name": item["name"], "calories": item["calories"]} for item in data["items"]]
    return jsonify(calories_data)


@app.route('/protein/<food>', methods=['GET'])
def get_protein(food):
    """
    Route to get protein information for a food item.
    """
    data = api_client.get_nutrition(food)  # Use get_nutrition directly here
    if "items" not in data:
        return jsonify({"error": "No data found"}), 404

    protein_data = [{"name": item["name"], "protein": item["protein_g"]} for item in data["items"]]
    return jsonify(protein_data)

@app.route('/carbohydrates/<food>', methods=['GET'])
def get_carbohydrates(food):
    """
    Route to get carbohydrate information for a food item.
    """
    data = api_client.get_nutrition(food)
    if "items" not in data:
        return jsonify({"error": "No data found"}), 404

    carbs_data = [{"name": item["name"], "carbohydrates": item["carbohydrates_total_g"]} for item in data["items"]]
    return jsonify(carbs_data)

@app.route('/sugar/<food>', methods=['GET'])
def get_sugar(food):
    """
    Route to get sugar information for a food item.
    """
    data = api_client.get_nutrition(food)
    if "items" not in data:
        return jsonify({"error": "No data found"}), 404

    sugar_data = [{"name": item["name"], "sugar": item["sugar_g"]} for item in data["items"]]
    return jsonify(sugar_data)

if __name__ == '__main__':
    app.run(debug=True)

