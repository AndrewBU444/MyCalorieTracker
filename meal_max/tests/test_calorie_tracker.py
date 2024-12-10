import pytest
from datetime import date
from calorie_tracker_model import CalorieTrackerModel
from db import db, CalorieIntake, WeightLog


@pytest.fixture
def setup_database(app):
    """Fixture to set up and tear down the database for tests."""
    with app.app_context():
        db.create_all()
        yield
        db.drop_all()


@pytest.fixture
def sample_user(setup_database):
    """Fixture to create a sample user."""
    user = CalorieTrackerModel(
        username="test_user",
        password="test_password",
        calorie_goal=2000,
        starting_weight=75.0
    )
    db.session.add(user)
    db.session.commit()
    return user


######################################################
#   Tests for User Management
######################################################

def test_create_user(setup_database):
    """Test creating a new user."""
    user = CalorieTrackerModel(
        username="new_user",
        password="secure_password",
        calorie_goal=2500,
        starting_weight=80.0
    )
    db.session.add(user)
    db.session.commit()

    # Verify the user is in the database
    saved_user = CalorieTrackerModel.query.filter_by(username="new_user").first()
    assert saved_user is not None
    assert saved_user.username == "new_user"
    assert saved_user.calorie_goal == 2500
    assert saved_user.starting_weight == 80.0


def test_find_user(sample_user):
    """Test finding an existing user."""
    user = CalorieTrackerModel.query.filter_by(username="test_user").first()
    assert user is not None
    assert user.username == "test_user"


def test_find_user_not_found(setup_database):
    """Test finding a non-existent user."""
    user = CalorieTrackerModel.query.filter_by(username="non_existent").first()
    assert user is None


######################################################
#   Tests for Logging Calories and Weight
######################################################

def test_log_calories(sample_user):
    """Test logging calorie intake for a user."""
    log_date = date.today()
    sample_user.log_calories(user_id=sample_user.id, calories=1800, log_date=log_date)

    # Verify the log is created
    log = CalorieIntake.query.filter_by(user_id=sample_user.id, date=log_date).first()
    assert log is not None
    assert log.calories == 1800
    assert log.date == log_date


def test_log_calories_duplicate_entry(sample_user):
    """Test logging calories for the same date raises an error."""
    log_date = date.today()
    sample_user.log_calories(user_id=sample_user.id, calories=1800, log_date=log_date)

    with pytest.raises(ValueError, match=f"Calorie log for {log_date} already exists"):
        sample_user.log_calories(user_id=sample_user.id, calories=2000, log_date=log_date)


def test_log_weight(sample_user):
    """Test logging weight for a user."""
    log_date = date.today()
    sample_user.log_weight(user_id=sample_user.id, weight=74.5, log_date=log_date)

    # Verify the log is created
    log = WeightLog.query.filter_by(user_id=sample_user.id, date=log_date).first()
    assert log is not None
    assert log.weight == 74.5
    assert log.date == log_date


######################################################
#   Tests for Summary Retrieval
######################################################

def test_get_user_summary(sample_user):
    """Test retrieving a user's summary."""
    log_date = date.today()
    sample_user.log_calories(user_id=sample_user.id, calories=1800, log_date=log_date)
    sample_user.log_weight(user_id=sample_user.id, weight=74.5, log_date=log_date)

    summary = sample_user.get_user_summary(username="test_user")

    assert summary["username"] == "test_user"
    assert summary["calorie_goal"] == 2000
    assert summary["starting_weight"] == 75.0
    assert len(summary["calorie_logs"]) == 1
    assert len(summary["weight_logs"]) == 1
    assert summary["calorie_logs"][0]["calories"] == 1800
    assert summary["weight_logs"][0]["weight"] == 74.5


def test_get_user_summary_no_logs(sample_user):
    """Test retrieving a user's summary with no logs."""
    summary = sample_user.get_user_summary(username="test_user")

    assert summary["username"] == "test_user"
    assert summary["calorie_goal"] == 2000
    assert summary["starting_weight"] == 75.0
    assert len(summary["calorie_logs"]) == 0
    assert len(summary["weight_logs"]) == 0
