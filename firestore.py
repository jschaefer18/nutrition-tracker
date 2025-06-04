from firebase_config import db
from datetime import datetime, timedelta

def log_nutrition(user_id, date_str, nutrition_data):
    date_doc = db.collection("users").document(user_id).collection("daily_logs").document(date_str)
    date_doc.set(nutrition_data)
    print(f"Log added for {user_id} on {date_str}")

def get_nutrition_log(user_id, date_str, print_log=True):
    doc_ref = db.collection("users").document(user_id).collection("daily_logs").document(date_str)
    doc = doc_ref.get()
    if doc.exists:
        log = doc.to_dict()
        if print_log:
            print(f"Log for {user_id} on {date_str}:\n{log}")
        return log
    else:
        if print_log:
            print(f"No log found for {user_id} on {date_str}")
        return None

def get_weekly_logs(user_id, end_date_str):
    end_date = datetime.strptime(end_date_str, "%Y-%m-%d")
    logs = []

    print(f"Weekly logs for {user_id} ({(end_date - timedelta(days=6)).date()} → {end_date.date()}):")

    for i in range(7):
        current_date = (end_date - timedelta(days=i)).strftime("%Y-%m-%d")
        log = get_nutrition_log(user_id, current_date, print_log=False)
        if log:
            log["date"] = current_date
            logs.append(log)

    logs.reverse()
    for entry in logs:
        print(entry)


    return logs

# Set nutrition goals for a user
def set_nutrition_goals(user_id, goals_data):
    user_ref = db.collection("users").document(user_id)
    user_ref.update({"goals": goals_data})
    print(f"🎯 Goals set for {user_id}")

# Get nutrition goals for a user
def get_nutrition_goals(user_id):
    user_ref = db.collection("users").document(user_id)
    doc = user_ref.get()
    if doc.exists:
        data = doc.to_dict()
        goals = data.get("goals", None)
        if goals:
            print(f"Goals for {user_id}:\n{goals}")
            return goals
        else:
            print("No goals set for this user.")
            return None
    else:
        print(f"User {user_id} not found.")
        return None
    
# Delete a daily log
def delete_nutrition_log(user_id, date_str):
    log_ref = db.collection("users").document(user_id).collection("daily_logs").document(date_str)
    log_ref.delete()
    print(f"🗑️ Deleted log for {user_id} on {date_str}")


