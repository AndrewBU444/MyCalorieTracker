#!/bin/bash

# Base URL for the Flask API
BASE_URL="http://localhost:5000/api"

# Helper function to check API responses
run_test() {
  local description=$1
  local method=$2
  local endpoint=$3
  local data=$4
  local expected=$5

  echo "$description"
  RESPONSE=$(curl -s -X "$method" "$BASE_URL$endpoint" -H "Content-Type: application/json" -d "$data")
  echo "Response: $RESPONSE"
  if echo "$RESPONSE" | grep -q "$expected"; then
    echo "PASS: $description"
  else
    echo "FAIL: $description"
    exit 1
  fi
}

# Smoke Test Suite
echo "Starting smoke tests..."

# Health and database checks
run_test "Checking service health" "GET" "/health" "" '"status": "healthy"'
run_test "Checking database connection" "GET" "/db-check" "" '"database_status": "healthy"'

# User management
run_test "Creating a new user" "POST" "/create-user" '{"username":"testuser", "password":"password123"}' '"status": "user added"'
run_test "Logging in the user" "POST" "/login" '{"username":"testuser", "password":"password123"}' '"message": "User testuser logged in successfully."'

# Major API functionality
run_test "Adding calorie intake" "POST" "/intake" '{"username": "testuser", "date": "2024-12-08", "calories": 500}' '"status": "intake added"'
run_test "Updating calorie goal" "POST" "/update-goal" '{"username": "testuser", "goal": 2500}' '"status": "goal updated"'
run_test "Retrieving user nutrition details" "GET" "/nutrition/testuser" "" '"nutrition":'

# Cleanup
run_test "Deleting the user" "DELETE" "/delete/testuser" "" '"status": "user deleted"'

echo "All smoke tests passed successfully!"