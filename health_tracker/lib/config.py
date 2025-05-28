import os
from datetime import datetime
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base, User, FoodEntry, Goal, MealPlan

# =============== DATABASE SETUP =====================
engine = create_engine("sqlite:///health_tracker.db")
Session = sessionmaker(bind=engine)
session = Session()

# Ensure tables are created
Base.metadata.create_all(engine)

# =============== USER OPERATIONS =====================
def create_user():
    name = input("Enter User Name: ")
    user = User(name=name)
    session.add(user)
    session.commit()
    print(f"User '{name}' created successfully.")

def list_users():
    users = session.query(User).all()
    for user in users:
        print(f"ID: {user.id} | Name: {user.name} | Created At: {user.created_at}")

# =============== FOOD ENTRY OPERATIONS =====================
def add_food_entry():
    user_name = input("Enter User Name: ")
    user = session.query(User).filter_by(name=user_name).first()
    if not user:
        print("User not found.")
        return

    food = input("Enter Food Name: ")
    calories = int(input("Enter Calories: "))
    date_input = input("Enter Date (YYYY-MM-DD): ")
    date = datetime.strptime(date_input, "%Y-%m-%d").date()

    entry = FoodEntry(food=food, calories=calories, date=date, user=user)
    session.add(entry)
    session.commit()
    print("Food entry added successfully.")

def list_food_entries():
    user_name = input("Enter User Name (leave blank for all): ").strip()
    date_input = input("Enter Date (YYYY-MM-DD) (optional): ").strip()

    query = session.query(FoodEntry)

    if user_name:
        user = session.query(User).filter_by(name=user_name).first()
        if not user:
            print("User not found.")
            return
        query = query.filter_by(user_id=user.id)

    if date_input:
        date = datetime.strptime(date_input, "%Y-%m-%d").date()
        query = query.filter_by(date=date)

    entries = query.all()
    for entry in entries:
        print(f"{entry.date} | {entry.food} | {entry.calories} cal | User: {entry.user.name}")

# =============== GOAL OPERATIONS =====================
def set_goals():
    user_name = input("Enter User Name: ")
    user = session.query(User).filter_by(name=user_name).first()
    if not user:
        print("User not found.")
        return

    daily = int(input("Enter Daily Calorie Goal: "))
    weekly = int(input("Enter Weekly Calorie Goal: "))

    goal = Goal(user=user, daily_calories=daily, weekly_calories=weekly)
    session.add(goal)
    session.commit()
    print("Goals set successfully.")

def list_goals():
    user_name = input("Enter User Name: ")
    user = session.query(User).filter_by(name=user_name).first()
    if not user:
        print("User not found.")
        return

    for goal in user.goals:
        print(f"Daily: {goal.daily_calories} | Weekly: {goal.weekly_calories} | Set on: {goal.set_date}")

# =============== MAIN MENU =====================
def main():
    while True:
        os.system("cls" if os.name == "nt" else "clear")
        print("=== Health Simplified CLI ===")
        print("1. Manage Users")
        print("2. Log/View Food Entries")
        print("3. Set/View Nutrition Goals")
        print("4. Exit")
        choice = input("Select an option: ")

        if choice == '1':
            os.system("cls" if os.name == "nt" else "clear")
            print("1. Create User")
            print("2. List Users")
            user_choice = input("Choice: ")
            if user_choice == '1':
                create_user()
            elif user_choice == '2':
                list_users()
            input("Press Enter to continue...")

        elif choice == '2':
            os.system("cls" if os.name == "nt" else "clear")
            print("1. Add Food Entry")
            print("2. List Food Entries")
            entry_choice = input("Choice: ")
            if entry_choice == '1':
                add_food_entry()
            elif entry_choice == '2':
                list_food_entries()
            input("Press Enter to continue...")

        elif choice == '3':
            os.system("cls" if os.name == "nt" else "clear")
            print("1. Set Goals")
            print("2. List Goals")
            goal_choice = input("Choice: ")
            if goal_choice == '1':
                set_goals()
            elif goal_choice == '2':
                list_goals()
            input("Press Enter to continue...")

        elif choice == '4':
            print("Exiting. Goodbye!")
            session.close()
            break
        else:
            print("Invalid option.")
            input("Press Enter to try again...")

# =============== ENTRY POINT =====================
if __name__ == "__main__":
    main()
