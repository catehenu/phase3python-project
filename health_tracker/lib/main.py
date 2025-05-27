import os
from datetime import datetime
from config import Session
from models import User, FoodEntry, Goal

# ========== USER OPERATIONS ==========
def create_user():
    name = input("Enter User Name: ")
    session = Session()
    user = User(name=name)
    session.add(user)
    session.commit()
    session.close()
    print(f"User '{name}' created successfully.")

def list_users():
    session = Session()
    users = session.query(User).all()
    for user in users:
        print(f"ID: {user.id} | Name: {user.name} | Created At: {user.created_at}")
    session.close()

# ========== FOOD ENTRY OPERATIONS ==========
def add_food_entry():
    session = Session()
    user_name = input("Enter User Name: ")
    user = session.query(User).filter_by(name=user_name).first()
    if not user:
        print("User not found.")
        session.close()
        return

    food = input("Enter Food Name: ")
    calories = int(input("Enter Calories: "))
    date_input = input("Enter Date (YYYY-MM-DD): ")
    date = datetime.strptime(date_input, "%Y-%m-%d").date()

    entry = FoodEntry(food=food, calories=calories, date=date, user=user)
    session.add(entry)
    session.commit()
    session.close()
    print("Food entry added successfully.")

def list_food_entries():
    session = Session()
    user_name = input("Enter User Name (optional): ").strip()
    date_input = input("Enter Date (YYYY-MM-DD) (optional): ").strip()

    query = session.query(FoodEntry)

    if user_name:
        user = session.query(User).filter_by(name=user_name).first()
        if not user:
            print("User not found.")
            session.close()
            return
        query = query.filter_by(user_id=user.id)

    if date_input:
        date = datetime.strptime(date_input, "%Y-%m-%d").date()
        query = query.filter_by(date=date)

    entries = query.all()
    for entry in entries:
        print(f"ID: {entry.id} | {entry.date} | {entry.food} | {entry.calories} cal | User: {entry.user.name}")
    session.close()

# ========== GOAL OPERATIONS ==========
def set_goal():
    session = Session()
    user_name = input("Enter User Name: ")
    user = session.query(User).filter_by(name=user_name).first()
    if not user:
        print("User not found.")
        session.close()
        return

    daily = int(input("Enter Daily Calorie Goal: "))
    weekly = int(input("Enter Weekly Calorie Goal: "))
    goal = Goal(user=user, daily_calories=daily, weekly_calories=weekly)
    session.add(goal)
    session.commit()
    session.close()
    print("Goal set successfully.")

def list_goals():
    session = Session()
    user_name = input("Enter User Name: ")
    user = session.query(User).filter_by(name=user_name).first()
    if not user:
        print("User not found.")
        session.close()
        return

    for goal in user.goals:
        print(f"Daily: {goal.daily_calories} | Weekly: {goal.weekly_calories} | Set On: {goal.set_date}")
    session.close()

# ========== MAIN MENU LOOP ==========
def main():
    while True:
        os.system("cls" if os.name == "nt" else "clear")
        print("=== Health Simplified CLI ===")
        print("1. Manage Users")
        print("2. Manage Food Entries")
        print("3. Manage Goals")
        print("4. Exit")

        main_choice = input("Select an option: ")

        if main_choice == '1':
            while True:
                os.system("cls" if os.name == "nt" else "clear")
                print("1. Create User")
                print("2. List Users")
                print("3. Back to Main Menu")
                user_choice = input("Select: ")
                if user_choice == '1':
                    create_user()
                elif user_choice == '2':
                    list_users()
                elif user_choice == '3':
                    break
                input("Press Enter to continue...")

        elif main_choice == '2':
            while True:
