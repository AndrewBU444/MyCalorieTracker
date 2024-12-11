from dataclasses import asdict, dataclass
from db import CalorieIntake, WeightLog
import logging
from typing import Any, List
from datetime import date
from sqlalchemy.orm import relationship

from sqlalchemy import event
from sqlalchemy.exc import IntegrityError

import logging 
from db import db
logger = logging.getLogger(__name__)


@dataclass
class CalorieTrackerModel(db.Model):
    """
    Represents a user in the calorie tracker application.

    Attributes:
        id (int): Primary key, unique identifier for each user.
        username (str): Unique username for the user.
        calorie_goal (int): Daily calorie goal set by the user.
        starting_weight (float): User's starting weight.
        salt (str): Salt used for password hashing.
        password_hash (str): Hashed password for the user.
        calorie_logs (relationship): Relationship to calorie intake logs.
        weight_logs (relationship): Relationship to weight logs.
    """
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    calorie_goal = db.Column(db.Integer, nullable=False)
    starting_weight = db.Column(db.Float, nullable=False)
    salt = db.Column(db.String(128), nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)

    # Relationships
    calorie_logs = relationship('CalorieIntake', backref='user', lazy=True)
    weight_logs = relationship('WeightLog', backref='user', lazy=True)

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
        """Generate a random salt for password hashing."""
        # Implement salt generation logic
        pass

    def generate_password_hash(self, password: str):
        """Generate a hashed password using the salt."""
        # Implement password hashing logic using self.salt
        pass

    def find_user(self, username: str):
        """
        Finds a user by their username.

        Args:
            username (str): Username to search for.

        Returns:
            CalorieTrackerModel: The user object if found.

        Raises:
            ValueError: If the user is not found.
        """
        user = CalorieTrackerModel.query.filter_by(username=username).first()
        if user:
            logger.info(f"User found: {username}")
            return user
        logger.error(f"User not found: {username}")
        raise ValueError(f"User not found: {username}")

    def log_calories(self, user_id: int, calories: int, log_date: date = None):
        """
        Logs calorie intake for a user.

        Args:
            user_id (int): ID of the user logging calories.
            calories (int): Number of calories consumed.
            log_date (date, optional): Date of the log. Defaults to today.

        Raises:
            ValueError: If calories are non-positive or a log for the date already exists.
        """
        if calories <= 0:
            raise ValueError("Calories must be a positive number")

        log_date = log_date or date.today()
        existing_log = CalorieIntake.query.filter_by(user_id=user_id, date=log_date).first()
        if existing_log:
            raise ValueError(f"Calorie log for {log_date} already exists")

        calorie_log = CalorieIntake(user_id=user_id, date=log_date, calories=calories)
        db.session.add(calorie_log)
        db.session.commit()

    def log_weight(self, user_id: int, weight: float, log_date: date = None):
        """
        Logs weight for the user.

        Args:
            user_id (int): ID of the user logging weight.
            weight (float): Weight of the user.
            log_date (date, optional): Date of the log. Defaults to today.

        Raises:
            ValueError: If weight is non-positive.
        """
        if weight <= 0:
            raise ValueError("Weight must be a positive number")

        log_date = log_date or date.today()
        weight_log = WeightLog(user_id=user_id, date=log_date, weight=weight)
        db.session.add(weight_log)
        db.session.commit()
        logger.info(f"Logged weight {weight} for user {user_id} on {log_date}.")

    def delete_calorie_log(self, log_id: int):
        """
        Deletes a calorie log by its ID.

        Args:
            log_id (int): ID of the calorie log to delete.

        Raises:
            ValueError: If the log does not exist.
        """
        log = CalorieIntake.query.get(log_id)
        if not log:
            logger.error(f"Calorie log with ID {log_id} not found.")
            raise ValueError("Calorie log not found.")
        db.session.delete(log)
        db.session.commit()
        logger.info(f"Deleted calorie log with ID {log_id}.")

    def get_user_summary(self, username: str):
        """
        Retrieves a summary of a user's calorie intake and weight logs.

        Args:
            username (str): Username of the user.

        Returns:
            dict: A summary of the user's details, calorie logs, and weight logs.
        """
        user = self.find_user(username)
        summary = {
            "username": user.username,
            "calorie_goal": user.calorie_goal,
            "starting_weight": user.starting_weight,
            "calorie_logs": user.calorie_logs,
            "weight_logs": user.weight_logs,
        }
        logger.info(f"Retrieved summary for {username}.")
        return summary