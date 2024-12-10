from flask import Blueprint, app, request, jsonify
from .models import User, CalorieIntake
from . import db
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

user_blueprint = Blueprint('user', __name__)

@user_blueprint.route('/create-account', methods=['POST'])
def create_account():
    # Implementation here
    ...

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
        return jsonify({'error': 'Username, password, calorie goal, and starting weight are required'}), 400

    existing_user = User.query.filter_by(username=username).first()
    if existing_user:
        return jsonify({'error': 'User already exists'}), 400

    hashed_password = generate_password_hash(password)  # Hash the password
    new_user = User(username=username, password=hashed_password, calorie_goal=calorie_goal, starting_weight=starting_weight)
    db.session.add(new_user)
    db.session.commit()
    return jsonify({'message': 'User created successfully'}), 201

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

# 5. Get calorie intake history
@app.route('/history/<username>', methods=['GET'])
def get_history(username):
    user = User.query.filter_by(username=username).first()
    if not user:
        return jsonify({'error': 'User not found'}), 404

    intakes = CalorieIntake.query.filter_by(user_id=user.id).order_by(CalorieIntake.date).all()
    history = [{'date': intake.date.strftime('%Y-%m-%d'), 'calories': intake.calories} for intake in intakes]

    return jsonify({
        'username': user.username,
        'calorie_goal': user.calorie_goal,
        'history': history
    }), 200

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

