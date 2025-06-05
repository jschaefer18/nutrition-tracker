# This file contains all Firestore interactions like logging nutrition data, retrieving logs, setting goals, etc.
# It includes create, read, update, and delete operations (CRUD) for user and nutrition data.
# Also provides analytics like weekly reviews and goal tracking.


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
def get_weekly_logs(user_id, end_date_str, print_logs=True):
    end_date = datetime.strptime(end_date_str, "%Y-%m-%d").date()
    start_date = end_date - timedelta(days=6)

    logs_ref = db.collection("users").document(user_id).collection("daily_logs")
    docs = logs_ref.stream()

    weekly_data = []
    for doc in docs:
        try:
            doc_date = datetime.strptime(doc.id, "%Y-%m-%d").date()
            if start_date <= doc_date <= end_date:
                log = doc.to_dict()
                log["date"] = doc.id
                weekly_data.append(log)
        except ValueError:
            continue  # skip documents with invalid ID format

    weekly_data.sort(key=lambda x: x["date"])

    if print_logs:
        print(f"Weekly logs for {user_id} ({start_date} → {end_date}):")
        for log in weekly_data:
            print(log)

    return weekly_data



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


def weekly_review(user_id: str, end_date: str):
    from datetime import datetime

    weekly_logs = get_weekly_logs(user_id, end_date, print_logs=False)
    user_ref = db.collection("users").document(user_id)
    user_doc = user_ref.get()

    if not user_doc.exists:
        print("User not found.")
        return

    goals = user_doc.to_dict().get("goals")
    if not goals:
        print("No goals set for this user.")
        return

    print(f"Weekly review for {user_id} ({weekly_logs[0]['date']} → {end_date}):")

    goal_keys = ["calories", "protein", "carbs", "fat"]
    tolerance = 0.1  # 10% tolerance range
    summary = {k: 0 for k in goal_keys}

    for log in weekly_logs:
        print(f"\nDay: {log['date']}")
        for key in goal_keys:
            actual = log.get(key, 0)
            target = goals.get(key, 0)
            min_range = target * (1 - tolerance)
            max_range = target * (1 + tolerance)

            hit = min_range <= actual <= max_range
            status = "✅" if hit else "❌"
            if hit:
                summary[key] += 1
            print(f"  {key.title()}: {actual} vs goal {target} {status}")

    print("\nSummary:")
    for key in goal_keys:
        print(f"  {key.title()} goal met {summary[key]} out of {len(weekly_logs)} days.")

    print("\nFeedback:")
    for key in goal_keys:
        rate = summary[key] / len(weekly_logs)
        if rate == 1:
            print(f"  Excellent work on your {key} goal! You nailed it every day.")
        elif rate >= 0.6:
            print(f"  Good effort on {key}. You're close — just a little more consistency.")
        else:
            print(f"  Let’s focus on improving your {key} intake next week.")


def set_goals(user_id, goals_dict):
    user_ref = db.collection("users").document(user_id)
    user_ref.update({"goals": goals_dict})
    print(f"Goals set for {user_id}")

def get_goals(user_id):
    user_ref = db.collection("users").document(user_id)
    doc = user_ref.get()
    if doc.exists:
        goals = doc.to_dict().get("goals")
        print(f"Goals for {user_id}:")
        print(goals)
        return goals
    else:
        print("User not found.")
        return None
