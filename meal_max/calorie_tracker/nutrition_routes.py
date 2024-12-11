from flask import Blueprint, app, jsonify
from api_client import CalorieNinjasAPIClient
import os

# Access the API key
API_KEY = os.getenv('API_KEY')
api_client = CalorieNinjasAPIClient(api_key=API_KEY)

nutrition_blueprint = Blueprint('nutrition', __name__)

@app.route('/nutrition/<food>', methods=['GET'])
def get_nutrition_route(food):
    """
    Route to get full nutrition information for a food item.

    Parameters:
        food (str): The name of the food item to get nutrition information for.

    Returns:
        JSON: A list of nutritional details for the specified food item, including:
              - name
              - calories
              - protein
              - carbohydrates
              - sugar
        HTTP Status Codes:
            - 200: Successful retrieval of nutrition data.
            - 404: No data found for the specified food item.
    """
    data = api_client.get_nutrition(food)  # Use the api_client instance

    if "items" not in data:
        return jsonify({"error": "No data found"}), 404
    
    nutrition_data = [
        {
            "name": item["name"],
            "calories": item["calories"],
            "protein": item["protein_g"],
            "carbohydrates": item["carbohydrates_total_g"],
            "sugar": item["sugar_g"]
        } for item in data["items"]
    ]
    return jsonify(nutrition_data)

@app.route('/calories/<food>', methods=['GET'])
def get_calories(food):
    """
    Route to get calorie information for a food item.

    Parameters:
        food (str): The name of the food item to get calorie information for.

    Returns:
        JSON: A list containing the name and calories for the specified food item.
        HTTP Status Codes:
            - 200: Successful retrieval of calorie data.
            - 404: No data found for the specified food item.
    """
    data = api_client.get_nutrition(food)
    if "items" not in data:
        return jsonify({"error": "No data found"}), 404
    
    calories_data = [{"name": item["name"], "calories": item["calories"]} for item in data["items"]]
    return jsonify(calories_data)


@app.route('/protein/<food>', methods=['GET'])
def get_protein(food):
    """
    Route to get protein information for a food item.

    Parameters:
        food (str): The name of the food item to get protein information for.

    Returns:
        JSON: A list containing the name and protein content for the specified food item.
        HTTP Status Codes:
            - 200: Successful retrieval of protein data.
            - 404: No data found for the specified food item.
    """
    data = api_client.get_nutrition(food)  # Use get_nutrition directly here
    if "items" not in data:
        return jsonify({"error": "No data found"}), 404

    protein_data = [{"name": item["name"], "protein": item["protein_g"]} for item in data["items"]]
    return jsonify(protein_data)

@app.route('/carbohydrates/<food>', methods=['GET'])
def get_carbohydrates(food):
    """
    Route to get carbohydrate information for a food item.

    Parameters:
        food (str): The name of the food item to get carbohydrate information for.

    Returns:
        JSON: A list containing the name and carbohydrate content for the specified food item.
        HTTP Status Codes:
            - 200: Successful retrieval of carbohydrate data.
            - 404: No data found for the specified food item.
    """
    data = api_client.get_nutrition(food)
    if "items" not in data:
        return jsonify({"error": "No data found"}), 404

    carbs_data = [{"name": item["name"], "carbohydrates": item["carbohydrates_total_g"]} for item in data["items"]]
    return jsonify(carbs_data)

@app.route('/sugar/<food>', methods=['GET'])
def get_sugar(food):
    """
    Route to get sugar information for a food item.

    Parameters:
        food (str): The name of the food item to get sugar information for.

    Returns:
        JSON: A list containing the name and sugar content for the specified food item.
        HTTP Status Codes:
            - 200: Successful retrieval of sugar data.
            - 404: No data found for the specified food item.
    """
    data = api_client.get_nutrition(food)
    if "items" not in data:
        return jsonify({"error": "No data found"}), 404

    sugar_data = [{"name": item["name"], "sugar": item["sugar_g"]} for item in data["items"]]
    return jsonify(sugar_data)

if __name__ == '__main__':
    app.run(debug=True)

