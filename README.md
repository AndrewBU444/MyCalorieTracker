# MyCalorieTracker

Our Calorie Tracker App is a tracker allows users to monitor their daily calorie intake and weight over time. This application allows users to create accounts, log calorie intake and weight, set and update calorie goals, and also track their progress. With the help of an external API, users can also retrieve nutritional information about the food items they consume, ensuring accurate tracking of their calorie intake.

The application integrates with the Calorie Ninjas API to fetch nutritional values for specific food items, providing precise insights into calories, proteins, carbohydrates, and sugars, which help users make informed dietary decisions.

## Routes Documentation:
### 1. Health Check 
- **Path**: `/api/health`
- **Request Type**: `GET`
- **Purpose**: Checks if the application is running.
- **Response Format**: `JSON`
- Example Response:
- Code: 200
- Content:
  ```json
  {
    "status": "healthy"
  }
---
### **2. Database Health Check**
- **Path**: `/api/db-check`
- **Request Type**: `GET`
- **Purpose**: Verifies database connection and table existence..
- **Response Format**: `JSON`
- Example Response:
- Code: 200
- Content:
  ```json
  {
    "database_status": "healthy"
  }
- Error Response Example:
- Code: 404
- Content:
- ```json
  {
    "error": "users table does not exist"
  }
---
### **3. Create Account**
- **Path**: `/create-account`
- **Request Type**: `POST`
- **Purpose**: Creates a new user account with calorie and weight tracking goals.
- **Response Format**: `JSON`
- Example Response:
- Code: 201
- Content:
  ```json
  {
    "message": "Account created successfully"
  }
- Error Response Example:
- Code: 400
- Content:
- ```json
  {
    "error": "All fields are required"
  }
---
### **5. Login (Authenticate User)**
- **Path**: `/login`
- **Request Type**: `POST`
- **Purpose**: Authenticates a user with their username and password.
- **Response Format**: `JSON`
- Example Response:
- Code: 200
- Content:
  ```json
  {
    "message": "Login successful"
  }
- Error Response Example:
- Code: 404
- Content:
- ```json
  {
    "error": "User not found"
  }
---
### **5. Login (Authenticate User)**
- **Path**: `/login`
- **Request Type**: `POST`
- **Purpose**: Authenticates a user with their username and password.
- **Response Format**: `JSON`
- Example Response:
- Code: 200
- Content:
  ```json
  {
    "message": "Login successful"
  }
- Error Response Example:
- Code: 404
- Content:
- ```json
  {
    "error": "User not found"
  }


  





