from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
import os

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///calorie_tracker.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Database Models
class User(db.Model):
    """
    Represents a user in the calorie tracker application.

    Attributes:
        id (int): Primary key, unique identifier for each user.
        username (str): Unique username for the user.
        calorie_goal (int): Daily calorie goal set by the user.
        starting_weight (float): User's starting weight.
        salt (str): Salt used for password hashing.
        password_hash (str): Hashed password for the user.
    """
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    calorie_goal = db.Column(db.Integer, nullable=False)
    starting_weight = db.Column(db.Integer, nullable=False)
    salt = db.Column(db.String(128), nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)

    def __init__(self, username, password, calorie_goal, starting_weight):
        """
        Initializes a new user with the provided details.

        Args:
            username (str): The username of the user.
            password (str): The raw password of the user.
            calorie_goal (int): Daily calorie goal set by the user.
            starting_weight (float): User's starting weight.
        """
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

    def __repr__(self):
        """Return a more readable representation of the User object"""
        return f"<User(username='{self.username}', calorie_goal={self.calorie_goal}, starting_weight={self.starting_weight})>"

# Routes

# 1. Register a user and set a calorie goal (Create Account)
@app.route('/create-account', methods=['POST'])
def create_account():
    """
    Create a new user account.

    Request:
        - username (str): The username for the account.
        - password (str): The password for the account.
        - calorie_goal (int): The daily calorie goal for the user.
        - starting_weight (float): The starting weight of the user.

    Response:
        - 201: Account created successfully.
        - 400: Missing fields or user already exists.
    """
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    calorie_goal = data.get('calorie_goal')
    starting_weight = data.get('starting_weight')

    if not username or not password or not calorie_goal or not starting_weight:
        return jsonify({'error': 'Username, password, calorie goal, and starting weight are required'}), 400

    existing_user = User.query.filter_by(username=username).first()
    if existing_user:
        return jsonify({'error': 'User already exists'}), 400

    new_user = User(username=username, password=password, calorie_goal=calorie_goal, starting_weight=starting_weight)
    db.session.add(new_user)
    db.session.commit()
    return jsonify({'message': 'User created successfully'}), 201

# 2. Login (Authenticate User)
@app.route('/login', methods=['POST'])
def login():
    """
    Authenticate a user with their username and password.

    Request:
        - username (str): The username for the account.
        - password (str): The password for the account.

    Response:
        - 200: Login successful.
        - 400: Missing fields.
        - 404: User not found.
        - 401: Invalid password.
    """
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return jsonify({'error': 'Username and password are required'}), 400

    user = User.query.filter_by(username=username).first()
    if not user:
        return jsonify({'error': 'User not found'}), 404

    # Check if the password matches the hashed password
    if not user.check_password(password):
        return jsonify({'error': 'Invalid password'}), 401

    return jsonify({'message': 'Login successful'}), 200

# 3. Update password
@app.route('/update-password', methods=['PUT'])
def update_password():
    """
    Update a user's password.

    Request:
        - username (str): The username for the account.
        - current_password (str): The current password of the user.
        - new_password (str): The new password to set.

    Response:
        - 200: Password updated successfully.
        - 400: Missing fields.
        - 404: User not found.
        - 401: Incorrect current password.
    """
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
    if not user.check_password(current_password):
        return jsonify({'error': 'Incorrect current password'}), 401

    # Hash the new password and update
    user.password_hash = user.generate_password_hash(new_password)
    db.session.commit()
    return jsonify({'message': 'Password updated successfully'}), 200

if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # Create database tables if they don't exist
    app.run(debug=True)
