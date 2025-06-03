import os
from datetime import datetime, timedelta
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base, User, FoodEntry, Goal, MealPlan

# ====== Database Setup ======
engine = create_engine("sqlite:///health_tracker.db")
Session = sessionmaker(bind=engine)
session = Session()
Base.metadata.create_all(engine)

# ====== User Operations ======
def create_user():
    name = input("Enter User Name: ").strip()
    if session.query(User).filter_by(name=name).first():
        print("User name already exists.")
        return
    user = User(name=name)
    session.add(user)
    session.commit()
    print(f"User '{name}' created successfully.")

def list_users():
    users = session.query(User).all()
    if not users:
        print("No users found.")
        return
    for u in users:
        print(f"ID: {u.id} | Name: {u.name} | Created: {u.created_at}")

def update_user():
    old_name = input("Enter current User Name: ").strip()
    user = session.query(User).filter_by(name=old_name).first()
    if not user:
        print("User not found.")
        return
    new_name = input("Enter new User Name: ").strip()
    user.name = new_name
    session.commit()
    print("User updated.")

def delete_user():
    name = input("Enter User Name to delete: ").strip()
    user = session.query(User).filter_by(name=name).first()
    if not user:
        print("User not found.")
        return
    session.delete(user)
    session.commit()
    print("User deleted.")

# ====== Food Entry Operations ======
def add_food_entry():
    user_name = input("Enter User Name: ").strip()
    user = session.query(User).filter_by(name=user_name).first()
    if not user:
        print("User not found.")
        return

    food = input("Food name: ").strip()
    try:
        calories = int(input("Calories (kcal): "))
    except ValueError:
        print("Calories must be a number.")
        return

    date_str = input("Date (YYYY-MM-DD): ").strip()
    try:
        date = datetime.strptime(date_str, "%Y-%m-%d").date()
    except:
        print("Invalid date format.")
        return

    entry = FoodEntry(food=food, calories=calories, date=date, user=user)
    session.add(entry)
    session.commit()
    print("Food entry added.")

def list_food_entries():
    user_name = input("Enter User Name (leave blank for all): ").strip()
    date_str = input("Date (YYYY-MM-DD): ").strip()
    try:
        date = datetime.strptime(date_str, "%Y-%m-%d").date()
    except:
        print("Invalid date format.")
        return

    query = session.query(FoodEntry).filter_by(date=date)
    if user_name:
        user = session.query(User).filter_by(name=user_name).first()
        if not user:
            print("User not found.")
            return
        query = query.filter_by(user_id=user.id)
    entries = query.all()
    if not entries:
        print("No entries found.")
        return
    print(f"\nFood entries on {date}:")
    for e in entries:
        print(f"{e.food} - {e.calories} kcal (User: {e.user.name})")

def daily_summary_report():
    user_name = input("Enter User Name: ").strip()
    user = session.query(User).filter_by(name=user_name).first()
    if not user:
        print("User not found.")
        return

    date_str = input("Date (YYYY-MM-DD): ").strip()
    try:
        date = datetime.strptime(date_str, "%Y-%m-%d").date()
    except:
        print("Invalid date format.")
        return

    entries = session.query(FoodEntry).filter_by(user_id=user.id, date=date).all()
    if not entries:
        print("No food entries for this date.")
        return

    total_calories = sum(e.calories for e in entries)
    latest_goal = session.query(Goal).filter_by(user_id=user.id).order_by(Goal.set_date.desc()).first()

    print(f"\nSummary for {user.name} on {date}:")
    for e in entries:
        print(f"- {e.food}: {e.calories} kcal")
    print(f"Total calories: {total_calories} kcal")
    if latest_goal:
        print(f"Daily Goal: {latest_goal.daily_calories} kcal")
        if total_calories > latest_goal.daily_calories:
            print("⚠️ Over your daily calorie goal!")
        else:
            print("✅ Within your daily goal.")
    else:
        print("No goals set yet.")

def update_food_entry():
    user_name = input("Enter User Name: ").strip()
    user = session.query(User).filter_by(name=user_name).first()
    if not user:
        print("User not found.")
        return

    date_str = input("Date (YYYY-MM-DD): ").strip()
    food_name = input("Food name to update: ").strip()
    try:
        date = datetime.strptime(date_str, "%Y-%m-%d").date()
    except:
        print("Invalid date format.")
        return

    entry = session.query(FoodEntry).filter_by(user_id=user.id, date=date, food=food_name).first()
    if not entry:
        print("Food entry not found.")
        return

    new_food = input("New food name: ").strip()
    try:
        new_calories = int(input("New calories: "))
    except:
        print("Invalid calorie input.")
        return

    entry.food = new_food
    entry.calories = new_calories
    session.commit()
    print("Food entry updated.")

def delete_food_entry():
    user_name = input("Enter User Name: ").strip()
    user = session.query(User).filter_by(name=user_name).first()
    if not user:
        print("User not found.")
        return

    date_str = input("Date (YYYY-MM-DD): ").strip()
    food_name = input("Food name to delete: ").strip()
    try:
        date = datetime.strptime(date_str, "%Y-%m-%d").date()
    except:
        print("Invalid date format.")
        return

    entry = session.query(FoodEntry).filter_by(user_id=user.id, date=date, food=food_name).first()
    if not entry:
        print("Food entry not found.")
        return

    session.delete(entry)
    session.commit()
    print("Food entry deleted.")

# ====== Goal Operations ======
def set_goals():
    user_name = input("Enter User Name: ").strip()
    user = session.query(User).filter_by(name=user_name).first()
    if not user:
        print("User not found.")
        return

    try:
        daily_goal = int(input("Enter daily calorie goal (kcal): "))
        weekly_goal = int(input("Enter weekly calorie goal (kcal): "))
    except:
        print("Please enter valid numbers.")
        return

    goal = Goal(user=user, daily_calories=daily_goal, weekly_calories=weekly_goal)
    session.add(goal)
    session.commit()
    print("Goals set.")

def list_goals():
    user_name = input("Enter User Name: ").strip()
    user = session.query(User).filter_by(name=user_name).first()
    if not user:
        print("User not found.")
        return

    if not user.goals:
        print("No goals set.")
        return

    for g in user.goals:
        print(f"Set on {g.set_date}: Daily = {g.daily_calories} kcal, Weekly = {g.weekly_calories} kcal")

def update_goal():
    user_name = input("Enter User Name: ").strip()
    user = session.query(User).filter_by(name=user_name).first()
    if not user:
        print("User not found.")
        return

    goal = session.query(Goal).filter_by(user_id=user.id).order_by(Goal.set_date.desc()).first()
    if not goal:
        print("No goals found.")
        return

    try:
        daily_goal = int(input(f"Enter new daily calorie goal (was {goal.daily_calories}): "))
        weekly_goal = int(input(f"Enter new weekly calorie goal (was {goal.weekly_calories}): "))
    except:
        print("Invalid input.")
        return

    goal.daily_calories = daily_goal
    goal.weekly_calories = weekly_goal
    session.commit()
    print("Goal updated.")

def delete_goal():
    user_name = input("Enter User Name: ").strip()
    user = session.query(User).filter_by(name=user_name).first()
    if not user:
        print("User not found.")
        return

    goal = session.query(Goal).filter_by(user_id=user.id).order_by(Goal.set_date.desc()).first()
    if not goal:
        print("No goals to delete.")
        return

    session.delete(goal)
    session.commit()
    print("Goal deleted.")

# ====== Meal Plan Operations ======

# Daily Meal Plan
def generate_daily_meal_plan():
    user_name = input("Enter User Name: ").strip()
    user = session.query(User).filter_by(name=user_name).first()
    if not user:
        print("User not found.")
        return

    date_str = input("Date for Meal Plan (YYYY-MM-DD): ").strip()
    try:
        date = datetime.strptime(date_str, "%Y-%m-%d").date()
    except:
        print("Invalid date format.")
        return

    # Remove existing meal plan for this date & user
    session.query(MealPlan).filter_by(user_id=user.id, day=date).delete()

    meal = input(f"Enter meal plan for {date.strftime('%A')} ({date}): ").strip()
    plan = MealPlan(user=user, day=date, meal=meal)
    session.add(plan)
    session.commit()
    print("Daily meal plan saved.")

def view_daily_meal_plan():
    user_name = input("Enter User Name: ").strip()
    user = session.query(User).filter_by(name=user_name).first()
    if not user:
        print("User not found.")
        return

    date_str = input("Date to view (YYYY-MM-DD): ").strip()
    try:
        date = datetime.strptime(date_str, "%Y-%m-%d").date()
    except:
        print("Invalid date format.")
        return

    plan = session.query(MealPlan).filter_by(user_id=user.id, day=date).first()
    if not plan:
        print("No meal plan found for this date.")
        return

    print(f"Meal Plan for {user.name} on {date}: {plan.meal}")

def update_meal_plan():
    user_name = input("Enter User Name: ").strip()
    user = session.query(User).filter_by(name=user_name).first()
    if not user:
        print("User not found.")
        return

    date_str = input("Date of meal plan to update (YYYY-MM-DD): ").strip()
    try:
        date = datetime.strptime(date_str, "%Y-%m-%d").date()
    except:
        print("Invalid date format.")
        return

    plan = session.query(MealPlan).filter_by(user_id=user.id, day=date).first()
    if not plan:
        print("Meal plan not found.")
        return

    new_meal = input("Enter updated meal plan: ").strip()
    plan.meal = new_meal
    session.commit()
    print("Meal plan updated.")

def delete_meal_plan():
    user_name = input("Enter User Name: ").strip()
    user = session.query(User).filter_by(name=user_name).first()
    if not user:
        print("User not found.")
        return

    date_str = input("Date of meal plan to delete (YYYY-MM-DD): ").strip()
    try:
        date = datetime.strptime(date_str, "%Y-%m-%d").date()
    except:
        print("Invalid date format.")
        return

    plan = session.query(MealPlan).filter_by(user_id=user.id, day=date).first()
    if not plan:
        print("Meal plan not found.")
        return

    session.delete(plan)
    session.commit()
    print("Meal plan deleted.")

# Weekly Meal Plan
def generate_weekly_meal_plan():
    user_name = input("Enter User Name: ").strip()
    user = session.query(User).filter_by(name=user_name).first()
    if not user:
        print("User not found.")
        return

    monday_str = input("Enter Monday Date of the week (YYYY-MM-DD): ").strip()
    try:
        monday = datetime.strptime(monday_str, "%Y-%m-%d").date()
    except:
        print("Invalid date format.")
        return

    if monday.weekday() != 0:
        print("Date is not a Monday.")
        return

    # Delete existing plans for that week
    for i in range(7):
        day = monday + timedelta(days=i)
        session.query(MealPlan).filter_by(user_id=user.id, day=day).delete()

    # Input meal plans for 7 days
    for i in range(7):
        day = monday + timedelta(days=i)
        meal = input(f"Meal plan for {day.strftime('%A')} ({day}): ").strip()
        plan = MealPlan(user=user, day=day, meal=meal)
        session.add(plan)

    session.commit()
    print("Weekly meal plan saved.")

def view_weekly_meal_plan():
    user_name = input("Enter User Name: ").strip()
    user = session.query(User).filter_by(name=user_name).first()
    if not user:
        print("User not found.")
        return

    monday_str = input("Enter Monday Date of the week to view (YYYY-MM-DD): ").strip()
    try:
        monday = datetime.strptime(monday_str, "%Y-%m-%d").date()
    except:
        print("Invalid date format.")
        return

    if monday.weekday() != 0:
        print("Date is not a Monday.")
        return

    print(f"\nWeekly Meal Plan for week starting {monday}:")
    for i in range(7):
        day = monday + timedelta(days=i)
        plan = session.query(MealPlan).filter_by(user_id=user.id, day=day).first()
        meal = plan.meal if plan else "(No plan)"
        print(f"{day.strftime('%A %Y-%m-%d')}: {meal}")

def update_weekly_meal_plan():
    print("To update weekly meal plan, regenerate it using 'Generate Weekly Meal Plan' option.")
    # Because updating partial weekly meal plans can be complex,
    # we advise regenerating the whole weekly plan.

def delete_weekly_meal_plan():
    user_name = input("Enter User Name: ").strip()
    user = session.query(User).filter_by(name=user_name).first()
    if not user:
        print("User not found.")
        return

    monday_str = input("Enter Monday Date of the week to delete (YYYY-MM-DD): ").strip()
    try:
        monday = datetime.strptime(monday_str, "%Y-%m-%d").date()
    except:
        print("Invalid date format.")
        return

    if monday.weekday() != 0:
        print("Date is not a Monday.")
        return

    for i in range(7):
        day = monday + timedelta(days=i)
        plan = session.query(MealPlan).filter_by(user_id=user.id, day=day).first()
        if plan:
            session.delete(plan)

    session.commit()
    print("Weekly meal plan deleted.")

# ====== Main CLI Loop ======
def main():
    while True:
        os.system("cls" if os.name == "nt" else "clear")
        print("=== Health Tracker ===")
        print("1. User Management")
        print("2. Food Entry Management")
        print("3. Goals Management")
        print("4. Meal Plan Management")
        print("5. Exit")

        choice = input("Select an option: ").strip()

        if choice == '1':
            while True:
                os.system("cls" if os.name == "nt" else "clear")
                print("=== User Management ===")
                print("1. Create User")
                print("2. List Users")
                print("3. Update User")
                print("4. Delete User")
                print("0. Back to Main Menu")
                ch = input("Select an option: ").strip()
                if ch == '1': create_user()
                elif ch == '2': list_users()
                elif ch == '3': update_user()
                elif ch == '4': delete_user()
                elif ch == '0': break
                input("\nPress Enter to continue...")

        elif choice == '2':
            while True:
                os.system("cls" if os.name == "nt" else "clear")
                print("=== Food Entry Management ===")
                print("1. Add Food Entry")
                print("2. List Food Entries")
                print("3. Daily Summary Report")
                print("4. Update Food Entry")
                print("5. Delete Food Entry")
                print("0. Back to Main Menu")
                ch = input("Select an option: ").strip()
                if ch == '1': add_food_entry()
                elif ch == '2': list_food_entries()
                elif ch == '3': daily_summary_report()
                elif ch == '4': update_food_entry()
                elif ch == '5': delete_food_entry()
                elif ch == '0': break
                input("\nPress Enter to continue...")

        elif choice == '3':
            while True:
                os.system("cls" if os.name == "nt" else "clear")
                print("=== Goals Management ===")
                print("1. Set Goals")
                print("2. List Goals")
                print("3. Update Goal")
                print("4. Delete Goal")
                print("0. Back to Main Menu")
                ch = input("Select an option: ").strip()
                if ch == '1': set_goals()
                elif ch == '2': list_goals()
                elif ch == '3': update_goal()
                elif ch == '4': delete_goal()
                elif ch == '0': break
                input("\nPress Enter to continue...")

        elif choice == '4':
            while True:
                os.system("cls" if os.name == "nt" else "clear")
                print("=== Meal Plan Management ===")
                print("1. Generate Daily Meal Plan")
                print("2. View Daily Meal Plan")
                print("3. Update Daily Meal Plan")
                print("4. Delete Daily Meal Plan")
                print("5. Generate Weekly Meal Plan")
                print("6. View Weekly Meal Plan")
                print("7. Update Weekly Meal Plan")
                print("8. Delete Weekly Meal Plan")
                print("0. Back to Main Menu")
                ch = input("Select an option: ").strip()
                if ch == '1': generate_daily_meal_plan()
                elif ch == '2': view_daily_meal_plan()
                elif ch == '3': update_meal_plan()
                elif ch == '4': delete_meal_plan()
                elif ch == '5': generate_weekly_meal_plan()
                elif ch == '6': view_weekly_meal_plan()
                elif ch == '7': update_weekly_meal_plan()
                elif ch == '8': delete_weekly_meal_plan()
                elif ch == '0': break
                input("\nPress Enter to continue...")

        elif choice == '5':
            print("Goodbye!")
            break

        else:
            print("Invalid choice. Try again.")
            input("\nPress Enter to continue...")

if __name__ == "__main__":
    main()
