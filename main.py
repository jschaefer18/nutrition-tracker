# main.py
# This is the main driver script for the Nutrition Tracker CLI.
# It handles user authentication and provides the menu interface for user interactions.

from auth import register_user, login_user
from firestore import (
    log_nutrition,
    get_weekly_logs,
    get_nutrition_log,
    set_goals,
    get_goals,
    delete_nutrition_log,
    weekly_review,
)
from datetime import datetime

# This menu allows the logged-in user to interact with their nutrition data.
def user_menu(user_id):
    while True:
        print(f"\n=== Hello, {user_id}! ===")
        print("[1] Log nutrition")
        print("[2] View this week’s logs")
        print("[3] Goals")
        print("[4] Weekly Review")
        print("[5] Delete a daily log")
        print("[6] Logout")
        choice = input("Choose an option: ")

        if choice == "1":
            log_nutrition_menu(user_id)

        elif choice == "2":
            today = datetime.today().strftime("%Y-%m-%d")
            get_weekly_logs(user_id, today)

        elif choice == "3":
            while True:
                print("\n--- Goals Menu ---")
                print("[1] Display current goals")
                print("[2] Set or update daily goals")
                print("[3] Go back")
                sub_choice = input("Choose an option: ")

                if sub_choice == "1":
                    get_goals(user_id)
                elif sub_choice == "2":
                    calories = int(input("Daily calorie goal: "))
                    protein = int(input("Daily protein goal (g): "))
                    carbs = int(input("Daily carbs goal (g): "))
                    fat = int(input("Daily fat goal (g): "))
                    set_goals(user_id, {
                        "calories": calories,
                        "protein": protein,
                        "carbs": carbs,
                        "fat": fat
                    })
                elif sub_choice == "3":
                    break
                else:
                    print("Invalid option.")

        elif choice == "4":
            today = datetime.today().strftime("%Y-%m-%d")
            weekly_review(user_id, today)

        elif choice == "5":
            date_str = input("Enter the date (YYYY-MM-DD) to delete: ")
            delete_nutrition_log(user_id, date_str)

        elif choice == "6":
            print("Logged out.")
            break

        else:
            print("Invalid choice. Try again.")

# Submenu for logging nutrition data
def log_nutrition_menu(user_id):
    while True:
        print("\n=== Log Nutrition ===")
        print("[1] Log for today")
        print("[2] Log for specific date")
        print("[3] Go back")
        sub_choice = input("Choose an option: ")

        if sub_choice == "1":
            date_str = datetime.today().strftime("%Y-%m-%d")
        elif sub_choice == "2":
            date_str = input("Enter the date (YYYY-MM-DD): ")
        elif sub_choice == "3":
            return
        else:
            print("Invalid choice.")
            continue

        calories = int(input("Calories: "))
        protein = int(input("Protein (g): "))
        carbs = int(input("Carbs (g): "))
        fat = int(input("Fat (g): "))
        meals = input("Meals (comma-separated): ").split(",")

        log_nutrition(user_id, date_str, {
            "calories": calories,
            "protein": protein,
            "carbs": carbs,
            "fat": fat,
            "meals": [m.strip() for m in meals],
        })

# This is the initial screen for login or signup
def main():
    while True:
        print("\n=== Welcome to Nutrition Tracker ===")
        print("[1] Login")
        print("[2] Sign up")
        print("[3] Quit")
        choice = input("Choose an option: ")

        if choice == "1":
            username = input("Username: ")
            password = input("Password: ")
            if login_user(username, password):
                user_menu(username)
            else:
                print("Login failed.")
        elif choice == "2":
            username = input("Choose a username: ")
            password = input("Choose a password: ")
            email = input("Email: ")
            name = input("Your name: ")
            daily_calories = int(input("Target daily calories: "))
            register_user(username, password, email, name, daily_calories)
        elif choice == "3":
            print("Goodbye!")
            break
        else:
            print("Invalid option.")

# Entrypoint
if __name__ == "__main__":
    main()
