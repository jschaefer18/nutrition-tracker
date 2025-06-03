from firestore import log_nutrition
from firestore import get_nutrition_log
from firestore import get_weekly_logs

def get_input_log():
    get_weekly_logs("user123", "2025-05-30")
    user_id = input("User ID: ")
    date_str = input("Date (YYYY-MM-DD): ")

    calories = int(input("Calories: "))
    protein = int(input("Protein (g): "))
    carbs = int(input("Carbs (g): "))
    fat = int(input("Fat (g): "))
    meals_input = input("Meals (comma-separated): ")
    meals = [m.strip() for m in meals_input.split(",")]

    nutrition_data = {
        "calories": calories,
        "protein": protein,
        "carbs": carbs,
        "fat": fat,
        "meals": meals
    }

    log_nutrition(user_id, date_str, nutrition_data)

# Run it
get_input_log()
