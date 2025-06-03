import firebase_admin
from firebase_admin import credentials, firestore
from datetime import datetime, timedelta

# Initialize Firebase (run this once)
cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred)
db = firestore.client()

def log_nutrition(user_id, date_str, nutrition_data):
    """
    Adds a daily nutrition log for a user.
    :param user_id: str (e.g., "user123")
    :param date_str: str (e.g., "2025-05-29")
    :param nutrition_data: dict of nutrition info
    """
    doc_ref = db.collection("users").document(user_id).collection("daily_logs").document(date_str)
    doc_ref.set(nutrition_data)
    print(f"Log added for {user_id} on {date_str}")


def get_nutrition_log(user_id, date_str, print_log=True):
    doc_ref = db.collection("users").document(user_id).collection("daily_logs").document(date_str)
    doc = doc_ref.get()

    if doc.exists:
        if print_log:
            print(f"Log for {user_id} on {date_str}:")
            print(doc.to_dict())
        return doc.to_dict()
    else:
        if print_log:
            print(f"No log found for {user_id} on {date_str}")
        return None




def get_weekly_logs(user_id, end_date_str):
    end_date = datetime.strptime(end_date_str, "%Y-%m-%d")
    start_date = end_date - timedelta(days=6)

    logs = []

    for i in range(7):
        current_date = start_date + timedelta(days=i)
        date_str = current_date.strftime("%Y-%m-%d")
        log = get_nutrition_log(user_id, date_str, print_log=False)


        if log:
            logs.append({
                "date": date_str,
                **log
            })

    if logs:
        print(f"\nWeekly logs for {user_id} ({start_date.date()} → {end_date.date()}):")
        for log in logs:
            print(log)
    else:
        print(f" No logs found for {user_id} in the past 7 days ending {end_date_str}")

    return logs
