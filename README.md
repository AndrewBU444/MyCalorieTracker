# MyCalorieTracker

## Overview

Our Calorie Tracker App is a tracker allows users to monitor their daily calorie intake and weight over time. This application allows users to create accounts, log calorie intake and weight, set and update calorie goals, and also track their progress. With the help of an external API, users can also retrieve nutritional information about the food items they consume, ensuring accurate tracking of their calorie intake.

The application integrates with the Calorie Ninjas API to fetch nutritional values for specific food items, providing precise insights into calories, proteins, carbohydrates, and sugars, which help users make informed dietary decisions.

## Key Features

### User Account Management
- **Create an account** with personalized calorie goals and starting weight.
- Ensure **username uniqueness** and securely store passwords.
- **Update account passwords** securely.
- **Log in** with an existing account using the correct credentials.

### Calorie Tracking
- **Record daily calorie intake** and review past entries.
- Retrieve **nutritional information** for food items, including:
  - Calories
  - Protein
  - Carbohydrates
  - Sugar content  
  (via the **CalorieNinjas API**)

### External API Integration
- Fetch detailed nutritional information for food items using the **CalorieNinjas API**.

## Steps to Run the Application

### 1. Generate an API Key
- Obtain an API key for the CalorieNinjas API from [https://calorieninjas.com/](https://calorieninjas.com/).
- Add the key to a `.env` file in the format:
API_KEY=<your_api_key>

### 2. Set Up the Environment
- Activate the virtual environment by running:
-./setup_env.sh

### 3. Start the Application
- Run the application using Docker:
-./run_docker.sh

### 4. Access the App
- The app will be running on the port specified in the `.env` file. If no port is specified, the default port is `8000`.

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
### **6. Update Password**
- **Path**: `/update-password`
- **Request Type**: `PUT`
- **Purpose**: Update the user's password.
- **Response Format**: `JSON`
- Example Response:
- Code: 200
- Content:
  ```json
  {
    "message": "Password updated successfully"
  }
- Error Response Example:
- Code: 401
- Content:
- ```json
  {
    "error": "Incorrect current password"
  }
- Error Response Example:
- Code: 401
- Content:
- ```json
  {
    "error": "User not found"
  }
- Error Response Example:
- Code: 400
- Content:
- ```json
  {
    "error": "Username, current password, and new password are required"
  }  
---
### **7. Add Daily Calorie Intake**
- **Path**: `/intake`
- **Request Type**: `POST`
- **Purpose**: Logs calorie intake for a specific user on a given date.
- **Response Format**: `JSON`
- **Request Format**:
  ```json
  {
  "username": "string",
  "date": "YYYY-MM-DD",
  "calories": "integer"
  }
- Example Response:
- Code: 201
- Content:
  ```json
  {
    "message": "Calorie intake added succesfully."
  }
- Error Response Example:
- Code: 400
- Content:
- ```json
  {
    "error": "Invalid date format. Use YYYY-MM-DD"
  }
- Error Response Example:
- Code: 404
- Content:
- ```json
  {
    "error": "User not found."
  }
- Error Response Example:
- Code: 40
- Content:
- ```json
  {
    "error": "Username, date, and calories are required."
  }
---
### **8. Get Calorie Intake History**
- **Path**: `/history/<username>`
- **Request Type**: `GET`
- **Purpose**: Retrieves calorie intake and weight logs for a user.
- **Response Format**: `JSON`
- Example Response:
- Code: 200
- Content:
  ```json
  {
  "username": "john_doe",
  "calorie_goal": 2000,
  "starting_weight": 75.5,
  "calorie_logs": [
    {
      "date": "2024-12-01",
      "calories": 1800
    }
  ],
  "weight_logs": [
    {
      "date": "2024-12-01",
      "weight": 75.0
    }
  ]
}
- Error Response Example:
- Code: 404
- Content:
- ```json
  {
    "error": "User not found"
  }
---

### **9. Update Calorie Goal**
- **Path**: `/goal`
- **Request Type**: `PUT`
- **Purpose**: Updates a user's calorie goal.
- **Response Format**: `JSON`
- **Request Format**:
  ```json
  {
  "username": "string",
  "calorie_goal": "integer"
  }
- Example Response:
- Code: 200
- Content:
  ```json
  {
    "message": "Calorie goal updated successfully"
  }
- Error Response Example:
- Code: 404
- Content:
- ```json
  {
    "error": "User not found"
  }
- Error Response Example:
- Code: 40
- Content:
- ```json
  {
    "error": "Username and new calorie goal are required"
  }
---
### **9. Update Goal**
- **Path**: `/goal`
- **Request Type**: `PUT`
- **Purpose**: Updates a user's calorie goal.
- **Response Format**: `JSON`
- Example Response:
- Code: 200
- Content:
  ```json
  {
    "message": "Calorie goal updated successfully"
  }
- Error Response Example:
- Code: 404
- Content:
- ```json
  {
    "error": "User not found"
  }
- Error Response Example:
- Code: 40
- Content:
- ```json
  {
    "error": "Username and new calorie goal are required"
  }
---
### **10. Delete User**
- **Path**: `/delete/<username>`
- **Request Type**: `DELETE`
- **Purpose**: Deletes a user and their associated logs.
- **Response Format**: `JSON`
- Example Response:
- Code: 200
- Content:
  ```json
  {
    "message": "User deleted successfully"
  }
- Error Response Example:
- Code: 404
- Content:
- ```json
  {
    "error": "User not found"
  }
---
### **11. Get Nutrition Information**
- **Path**: `/nutrition/<food>`
- **Request Type**: `GET`
- **Purpose**: Retrieves nutritional information for a specific food item.
- **Response Format**: `JSON`
- Example Response:
- Code: 200
- Content:
  ```json
  [
  {
    "name": "banana",
    "calories": 89,
    "protein": 1.1,
    "carbohydrates": 22.8,
    "sugar": 12.2
  }
]
- Error Response Example:
- Code: 404
- Content:
- ```json
  {
  "error": "No data found"
  }
---
### **12. Get Calories Information**
- **Path**: `/calories/<food>`
- **Request Type**: `GET`
- **Purpose**: Retrieves calorie information for a specific food item.
- **Response Format**: `JSON`
- **Example Response**:
  - **Code**: 200
  - **Content**:
    ```json
    [
      {
        "name": "banana",
        "calories": 89
      }
    ]
    ```
- **Error Response Example**:
  - **Code**: 404
  - **Content**:
    ```json
    {
      "error": "No data found"
    }
    ```
---
### **13. Get Protein Information**
- **Path**: `/protein/<food>`
- **Request Type**: `GET`
- **Purpose**: Retrieves protein information for a specific food item.
- **Response Format**: `JSON`
- **Example Response**:
  - **Code**: 200
  - **Content**:
    ```json
    [
      {
        "name": "banana",
        "protein": 1.1
      }
    ]
    ```
- **Error Response Example**:
  - **Code**: 404
  - **Content**:
    ```json
    {
      "error": "No data found"
    }
    ```

---

### **14. Get Carbohydrates Information**
- **Path**: `/carbohydrates/<food>`
- **Request Type**: `GET`
- **Purpose**: Retrieves carbohydrate information for a specific food item.
- **Response Format**: `JSON`
- **Example Response**:
  - **Code**: 200
  - **Content**:
    ```json
    [
      {
        "name": "banana",
        "carbohydrates": 22.8
      }
    ]
    ```
- **Error Response Example**:
  - **Code**: 404
  - **Content**:
    ```json
    {
      "error": "No data found"
    }
    ```
---

### **15. Get Sugar Information**
- **Path**: `/sugar/<food>`
- **Request Type**: `GET`
- **Purpose**: Retrieves sugar information for a specific food item.
- **Response Format**: `JSON`
- **Example Response**:
  - **Code**: 200
  - **Content**:
    ```json
    [
      {
        "name": "banana",
        "sugar": 12.2
      }
    ]
    ```
- **Error Response Example**:
  - **Code**: 404
  - **Content**:
    ```json
    {
      "error": "No data found"
    }
    ```

---





