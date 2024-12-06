from flask import Flask, request, jsonify,make_response, Response 
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from dotenv import load_dotenv
from config import ProductionConfig

# Load environment variables from .env file
load_dotenv()

def create_app(config_class=ProductionConfig):
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)  # Initialize db with app
    with app.app_context():
        db.create_all()  # Recreate all tables


    ####################################################
    #
    # Healthchecks
    #
    ####################################################


    @app.route('/api/health', methods=['GET'])
    def healthcheck() -> Response:
        """
        Health check route to verify the service is running.

        Returns:
            JSON response indicating the health status of the service.
        """
        app.logger.info('Health check')
        return make_response(jsonify({'status': 'healthy'}), 200)

# Initialize the Flask app
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///calorie_tracker.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize the database
db = SQLAlchemy(app)

# Define database models
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    calorie_goal = db.Column(db.Integer, nullable=False)
    starting_weight = db.Column(db.Integrer, nullable=False)

class CalorieIntake(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    date = db.Column(db.Date, nullable=False)
    calories = db.Column(db.Integer, nullable=False)

# Create the database tables
with app.app_context():
    db.create_all()

# Routes

# 1. Register a user and set a calorie goal
@app.route('/register', methods=['POST'])
def register_user():
    data = request.get_json()
    username = data.get('username')
    calorie_goal = data.get('calorie_goal')
    starting_weight = data.get('starting_weight')

    if not username or not calorie_goal or not starting_weight:
        return jsonify({'error': 'Username and calorie goal are required'}), 400

    existing_user = User.query.filter_by(username=username).first()
    if existing_user:
        return jsonify({'error': 'User already exists'}), 400

    new_user = User(username=username, calorie_goal=calorie_goal, starting_weight=starting_weight)
    db.session.add(new_user)
    db.session.commit()
    return jsonify({'message': 'User registered successfully'}), 201

# 2. Add daily calorie intake
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

# 3. Get calorie intake history
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

# 4. Update calorie goal
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

# 5. Delete user (optional)
@app.route('/delete/<username>', methods=['DELETE'])
def delete_user(username):
    user = User.query.filter_by(username=username).first()
    if not user:
        return jsonify({'error': 'User not found'}), 404

    CalorieIntake.query.filter_by(user_id=user.id).delete()
    db.session.delete(user)
    db.session.commit()
    return jsonify({'message': 'User deleted successfully'}), 200

# Run the app
if __name__ == '__main__':
    app = create_app()
    app.run(debug=True, host='0.0.0.0', port=5000)
