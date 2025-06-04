from auth import register_user, login_user
from firestore import (
    log_nutrition,
    get_weekly_logs,
    get_nutrition_goals,
    set_nutrition_goals,
    delete_nutrition_log,
)
from datetime import datetime

def log_today(user_id):
    date_str = datetime.today().strftime('%Y-%m-%d')
    print(f"\nLogging nutrition for {date_str}")
    calories = int(input("Calories: "))
    protein = int(input("Protein (g): "))
    carbs = int(input("Carbs (g): "))
    fat = int(input("Fat (g): "))
    meals_input = input("Meals (comma-separated): ")
    meals = [m.strip() for m in meals_input.split(",")]

    data = {
        "calories": calories,
        "protein": protein,
        "carbs": carbs,
        "fat": fat,
        "meals": meals
    }

    log_nutrition(user_id, date_str, data)

def view_or_update_goals(user_id):
    current_goals = get_nutrition_goals(user_id)
    print(f"\nCurrent goals for {user_id}: {current_goals}")
    update = input("Would you like to update your goals? (y/n): ").lower()
    if update == 'y':
        calories = int(input("New daily calorie goal: "))
        protein = int(input("New daily protein goal (g): "))
        carbs = int(input("New daily carbs goal (g): "))
        fat = int(input("New daily fat goal (g): "))
        new_goals = {
            "calories": calories,
            "protein": protein,
            "carbs": carbs,
            "fat": fat
        }
        set_nutrition_goals(user_id, new_goals)

def delete_log(user_id):
    date_str = input("Enter date to delete log (YYYY-MM-DD): ")
    delete_nutrition_log(user_id, date_str)

def logged_in_menu(user_id):
    while True:
        print(f"\n=== Hello, {user_id}! ===")
        print("[1] Log today's nutrition")
        print("[2] View this week's logs")
        print("[3] View or update daily goals")
        print("[4] Delete a nutrition log")
        print("[5] Logout")
        choice = input("Choose an option: ")

        if choice == '1':
            log_today(user_id)
        elif choice == '2':
            today = datetime.today().strftime('%Y-%m-%d')
            get_weekly_logs(user_id, today)
        elif choice == '3':
            view_or_update_goals(user_id)
        elif choice == '4':
            delete_log(user_id)
        elif choice == '5':
            print("Logged out.")
            break
        else:
            print("Invalid choice.")

def main():
    while True:
        print("\n=== Welcome to Nutrition Tracker ===")
        print("[1] Login")
        print("[2] Sign Up")
        print("[3] Quit")
        choice = input("Choose an option: ")

        if choice == '1':
            username = input("Username: ")
            password = input("Password: ")
            if login_user(username, password):
                logged_in_menu(username)
            else:
                print("Login failed.")
        elif choice == '2':
            username = input("Choose a username: ")
            password = input("Choose a password: ")
            email = input("Email: ")
            name = input("Full Name: ")
            age = int(input("Age: "))
            calorie_goal = int(input("Daily Calorie Goal: "))
            register_user(username, password, email, name, age, calorie_goal)
        elif choice == '3':
            print("Goodbye!")
            break
        else:
            print("Invalid choice.")

if __name__ == "__main__":
    main()
