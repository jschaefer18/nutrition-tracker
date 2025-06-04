import bcrypt
from firebase_config import db

def hash_password(password):
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

def check_password(password, hashed):
    return bcrypt.checkpw(password.encode('utf-8'), hashed.encode('utf-8'))

def register_user(username, password, email, name, age, goal_calories):
    doc_ref = db.collection("users").document(username)
    if doc_ref.get().exists:
        print("Username already taken.")
        return False

    hashed_pw = hash_password(password)
    user_data = {
        "email": email,
        "name": name,
        "age": age,
        "goal_calories": goal_calories,
        "password": hashed_pw
    }
    doc_ref.set(user_data)
    print(f"Registered user {username}")
    return True

def login_user(username, password):
    doc_ref = db.collection("users").document(username)
    doc = doc_ref.get()
    if not doc.exists:
        print("User not found.")
        return False

    stored_hash = doc.to_dict().get("password", "")
    if check_password(password, stored_hash):
        print("Login successful!")
        return True
    else:
        print("Invalid password.")
        return False
