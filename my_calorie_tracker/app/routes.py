from flask import Blueprint, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from meal_max.db import db
from app.models import Users
import logging

# Create a Flask Blueprint
auth_bp = Blueprint('auth', __name__)

# Logger setup
logger = logging.getLogger(__name__)

@auth_bp.route('/login', methods=['POST'])
def login():
    """
    Route to login a user by checking the password against the stored hash.
    """
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return jsonify({"error": "Username and password are required"}), 400

    try:
        user = Users.query.filter_by(username=username).first()
        if not user:
            return jsonify({"error": "User not found"}), 404
        
        if check_password_hash(user.password, password):
            return jsonify({"message": "Login successful"}), 200
        else:
            return jsonify({"error": "Incorrect password"}), 401
    except Exception as e:
        logger.error(f"Error in login: {str(e)}")
        return jsonify({"error": "Internal server error"}), 500


@auth_bp.route('/create-account', methods=['POST'])
def create_account():
    """
    Route to register a new user with a username and password.
    """
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return jsonify({"error": "Username and password are required"}), 400

    try:
        # Check if user already exists
        existing_user = Users.query.filter_by(username=username).first()
        if existing_user:
            return jsonify({"error": "User already exists"}), 400

        # Hash the password before storing it
        hashed_password = generate_password_hash(password)
        
        # Create new user
        new_user = Users(username=username, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()

        return jsonify({"message": "User created successfully"}), 201
    except Exception as e:
        logger.error(f"Error in create-account: {str(e)}")
        return jsonify({"error": "Internal server error"}), 500


@auth_bp.route('/update-password', methods=['PUT'])
def update_password():
    """
    Route to allow users to update their password.
    """
    data = request.get_json()
    username = data.get('username')
    old_password = data.get('old_password')
    new_password = data.get('new_password')

    if not username or not old_password or not new_password:
        return jsonify({"error": "Username, old password, and new password are required"}), 400

    try:
        user = Users.query.filter_by(username=username).first()
        if not user:
            return jsonify({"error": "User not found"}), 404

        if not check_password_hash(user.password, old_password):
            return jsonify({"error": "Incorrect old password"}), 401
        
        # Hash the new password before storing it
        new_hashed_password = generate_password_hash(new_password)
        user.password = new_hashed_password
        db.session.commit()

        return jsonify({"message": "Password updated successfully"}), 200
    except Exception as e:
        logger.error(f"Error in update-password: {str(e)}")
        return jsonify({"error": "Internal server error"}), 500
