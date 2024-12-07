import pytest
from app import create_app, db
from api_client import CalorieNinjasAPIClient

@pytest.fixture
def app():
    app = create_app()  # Initialize the Flask app
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'  # Use a test database
    db.create_all()  # Create the tables
    yield app
    db.session.remove()
    db.drop_all()

@pytest.fixture
def client(app):
    return app.test_client()  # This returns the Flask test client

def test_healthcheck(client):
    """Test the healthcheck route"""
    response = client.get('/api/health')
    assert response.status_code == 200
    assert b'"status": "healthy"' in response.data

def test_register_user(client):
    """Test registering a user"""
    data = {
        "username": "testuser",
        "calorie_goal": 2000,
        "starting_weight": 150
    }
    response = client.post('/register', json=data)
    assert response.status_code == 201
    assert b'"message": "User registered successfully"' in response.data

def test_add_calorie_intake(client):
    """Test adding calorie intake"""
    data = {
        "username": "testuser",
        "date": "2024-12-07",
        "calories": 500
    }
    response = client.post('/intake', json=data)
    assert response.status_code == 201
    assert b'"message": "Calorie intake added successfully"' in response.data

def test_get_nutrition(client, mocker):
    """Test fetching nutrition data for a food item"""
    # Mock the external API call to return controlled data
    mock_response = {
        "items": [
            {
                "name": "Apple",
                "calories": 95,
                "protein_g": 0.5,
                "carbohydrates_total_g": 25,
                "sugar_g": 19
            }
        ]
    }
    
    # Mock the get_nutrition function
    mocker.patch.object(get_nutrition, 'get_nutrition', return_value=mock_response)

    response = client.get('/nutrition/Apple')
    assert response.status_code == 200
    assert b'"name": "Apple"' in response.data
    assert b'"calories": 95' in response.data

