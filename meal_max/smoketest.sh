#!/bin/bash

# Define the base URL for the Flask API
BASE_URL="http://localhost:5000/api"

# Flag to control whether to echo JSON output
ECHO_JSON=false

# Parse command-line arguments
while [ "$#" -gt 0 ]; do
  case $1 in
    --echo-json) ECHO_JSON=true ;;
    *) echo "Unknown parameter passed: $1"; exit 1 ;;
  esac
  shift
done


###############################################
#
# Health checks
#
###############################################

# Function to check the health of the service
check_health() {
  echo "Checking health status..."
  curl -s -X GET "$BASE_URL/health" | grep -q '"status": "healthy"'
  if [ $? -eq 0 ]; then
    echo "Service is healthy."
  else
    echo "Health check failed."
    exit 1
  fi
}

# Function to check the database connection
check_db() {
  echo "Checking database connection..."
  curl -s -X GET "$BASE_URL/db-check" | grep -q '"database_status": "healthy"'
  if [ $? -eq 0 ]; then
    echo "Database connection is healthy."
  else
    echo "Database check failed."
    exit 1
  fi
}

##############################################
#
# User management
#
##############################################

# Function to create an account
create_account() {
  echo "Creating a new user..."
  curl -s -X POST "$BASE_URL/create-user" -H "Content-Type: application/json" \
    -d '{"username":"testuser", "password":"password123"}' | grep -q '"status": "user added"'
  if [ $? -eq 0 ]; then
    echo "User created successfully."
  else
    echo "Failed to create user."
    exit 1
  fi
}

# Function to log in a user
login() {
  echo "Logging in user..."
  response=$(curl -s -X POST "$BASE_URL/login" -H "Content-Type: application/json" \
    -d '{"username":"testuser", "password":"password123"}')
  if echo "$response" | grep -q '"message": "User testuser logged in successfully."'; then
    echo "User logged in successfully."
    if [ "$ECHO_JSON" = true ]; then
      echo "Login Response JSON:"
      echo "$response" | jq .
    fi
  else
    echo "Failed to log in user."
    if [ "$ECHO_JSON" = true ]; then
      echo "Error Response JSON:"
      echo "$response" | jq .
    fi
    exit 1
  fi
}

# Function to update the password
update_password() {
  echo "Updating password..."
  RESPONSE=$(curl -s -X POST "$BASE_URL/update-password" -H "Content-Type: application/json" \
    -d '{"username": "testuser", "old_password": "password123", "new_password": "newpassword456"}')
  echo "Response: $RESPONSE"
  echo "$RESPONSE" | grep -q '"status": "password updated"'
  if [ $? -eq 0 ]; then
    echo "PASS: Password updated successfully."
  else
    echo "FAIL: Failed to update password."
    exit 1
  fi
}

#Function to delete a user 
delete_user(){
   echo "Deleting the user..."
  RESPONSE=$(curl -s -X DELETE "$BASE_URL/delete/testuser")
  echo "Response: $RESPONSE"
  echo "$RESPONSE" | grep -q '"status": "user deleted"'
  if [ $? -eq 0 ]; then
    echo "PASS: User deleted successfully."
  else
    echo "FAIL: Failed to delete user."
    exit 1
  fi
}

##############################################
#
# Nutrients
#
##############################################

#Function to add a calorie intake
 add_calorie_intake(){
  echo "Adding calorie intake..."
  curl -s -X POST "$BASE_URL/intake" -H "Content-Type: application/json" \
    -d '{"username": "testuser", "date": "2024-12-08", "calories": 500}' | grep -q '"status": "intake added"'
  if [ $? -eq 0 ]; then
    echo "PASS: Calorie intake added successfully."
  else
    echo "FAIL: Failed to add calorie intake."
    exit 1
  fi
 }

#Function to get calorie intake history
get_history(){
  echo "Fetching user history..."
  RESPONSE=$(curl -s -X GET "$BASE_URL/history/testuser")
  echo "Response: $RESPONSE"
  echo "$RESPONSE" | grep -q '"history"'
  if [ $? -eq 0 ]; then
    echo "PASS: User history retrieved successfully."
  else
    echo "FAIL: Failed to retrieve user history."
    exit 1
  fi
}

# Function to update the calorie goal
update_goal() {
  echo "Updating calorie goal..."
  RESPONSE=$(curl -s -X POST "$BASE_URL/update-goal" -H "Content-Type: application/json" \
    -d '{"username": "testuser", "goal": 2500}')
  echo "Response: $RESPONSE"
  echo "$RESPONSE" | grep -q '"status": "goal updated"'
  if [ $? -eq 0 ]; then
    echo "PASS: Calorie goal updated to 2500."
  else
    echo "FAIL: Failed to update calorie goal."
    exit 1
  fi
}

# Function to get nutrition information
get_nutrition_route() {
  echo "Fetching nutrition details..."
  RESPONSE=$(curl -s -X GET "$BASE_URL/nutrition/testuser")
  echo "Response: $RESPONSE"
  echo "$RESPONSE" | grep -q '"nutrition":'
  if [ $? -eq 0 ]; then
    echo "PASS: Nutrition details retrieved."
  else
    echo "FAIL: Could not retrieve nutrition details."
    exit 1
  fi
}

# Function to get total calories
get_calories(){
  echo "Fetching total calories..."
  RESPONSE=$(curl -s -X GET "$BASE_URL/calories/testuser")
  echo "Response: $RESPONSE"
  echo "$RESPONSE" | grep -q '"calories":'
  if [ $? -eq 0 ]; then
    echo "PASS: Calories retrieved successfully."
  else
    echo "FAIL: Could not retrieve calories."
    exit 1
  fi
}

# Function to get protein
get_protein() {
  echo "Getting total protein..."
  RESPONSE=$(curl -s -X GET "$BASE_URL/protein/testuser")
  echo "Response: $RESPONSE"
  echo "$RESPONSE" | grep -q '"protein"'
  if [ $? -eq 0 ]; then
    echo "PASS: Total protein retrieved successfully."
  else
    echo "FAIL: Failed to retrieve total protein."
    exit 1
  fi
}

# Function to get carbohydrates
get_carbohydrates() {
  echo "Getting total carbohydrates..."
  RESPONSE=$(curl -s -X GET "$BASE_URL/carbohydrates/testuser")
  echo "Response: $RESPONSE"
  echo "$RESPONSE" | grep -q '"carbohydrates"'
  if [ $? -eq 0 ]; then
    echo "PASS: Total carbohydrates retrieved successfully."
  else
    echo "FAIL: Failed to retrieve total carbohydrates."
    exit 1
  fi
}


#Function to get sugar 
get_sugar() {
  echo "Getting total sugar..."
  RESPONSE=$(curl -s -X GET "$BASE_URL/sugar/testuser")
  echo "Response: $RESPONSE"
  echo "$RESPONSE" | grep -q '"sugar"'
  if [ $? -eq 0 ]; then
    echo "PASS: Total sugar retrieved successfully."
  else
    echo "FAIL: Failed to retrieve total sugar."
    exit 1
  fi
}



# Run all the steps in order
check_health
check_db
create_account
login
add_calorie_intake
update_goal
update_password
get_nutrition_route
get_calories
get_protein
get_carbohydrates
get_sugar


echo "All tests passed successfully!"
