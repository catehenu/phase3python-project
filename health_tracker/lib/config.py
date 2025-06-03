import os
from datetime import datetime, timedelta, date as dt_date
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base, User, FoodEntry, Goal, MealPlan

# =============== DATABASE SETUP =====================
engine = create_engine("sqlite:///health_tracker.db")
Session = sessionmaker(bind=engine)
session = Session()

Base.metadata.create_all(engine)

# =============== USER OPERATIONS =====================
def create_user():
    name = input("Enter User Name: ")
    existing_user = session.query(User).filter_by(name=name).first()
    if existing_user:
        print("User name already exists. Please choose another name.")
        return
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
    calories = int(input("Enter Calories (in kcal): "))
    date_input = input("Enter Date (YYYY-MM-DD): ")
    date = datetime.strptime(date_input, "%Y-%m-%d").date()

    entry = FoodEntry(food=food, calories=calories, date=date, user=user)
    session.add(entry)
    session.commit()
    print("Food entry added successfully.")

def list_food_entries():
    user_name = input("Enter User Name (leave blank for all): ").strip()
    date_input = input("Enter Date to View (YYYY-MM-DD): ").strip()

    try:
        view_date = datetime.strptime(date_input, "%Y-%m-%d").date()
    except ValueError:
        print("Invalid date format. Please use YYYY-MM-DD.")
        return

    query = session.query(FoodEntry).filter_by(date=view_date)

    if user_name:
        user = session.query(User).filter_by(name=user_name).first()
        if not user:
            print("User not found.")
            return
        query = query.filter_by(user_id=user.id)

    entries = query.all()
    if not entries:
        print(f"No entries found for {view_date}.")
        return

    print(f"\nFood Entries for {view_date}:")
    for entry in entries:
        print(f"{entry.food} | {entry.calories} kcal | User: {entry.user.name}")

def daily_summary_report():
    user_name = input("Enter User Name: ")
    user = session.query(User).filter_by(name=user_name).first()
    if not user:
        print("User not found.")
        return

    date_input = input("Enter date (YYYY-MM-DD): ").strip()
    try:
        summary_date = datetime.strptime(date_input, "%Y-%m-%d").date()
    except ValueError:
        print("Invalid date format.")
        return

    entries = session.query(FoodEntry).filter_by(user_id=user.id, date=summary_date).all()
    total_calories = sum(e.calories for e in entries)

    latest_goal = session.query(Goal).filter_by(user_id=user.id).order_by(Goal.set_date.desc()).first()

    print(f"\n== Summary for {user.name} on {summary_date} ==")
    for e in entries:
        print(f"- {e.food}: {e.calories} kcal")
    print(f"\nTotal: {total_calories} kcal")

    if latest_goal:
        print(f"Daily Goal: {latest_goal.daily_calories} kcal")
        if total_calories > latest_goal.daily_calories:
            print("⚠️ Over your daily goal!")
        else:
            print("✅ Within your goal!")
    else:
        print("⚠️ No goals set yet.")
        choice = input("Would you like to set your goals now? (y/n): ").strip().lower()
        if choice == 'y':
            set_goals()

# =============== GOAL OPERATIONS =====================
def set_goals():
    user_name = input("Enter User Name: ")
    user = session.query(User).filter_by(name=user_name).first()
    if not user:
        print("User not found.")
        return

    daily = int(input("Enter Daily Calorie Goal (in kcal): "))
    weekly = int(input("Enter Weekly Calorie Goal (in kcal): "))

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
        print(f"Daily: {goal.daily_calories} kcal | Weekly: {goal.weekly_calories} kcal | Set on: {goal.set_date}")

# =============== MEAL PLAN OPERATIONS =====================
def generate_daily_meal_plan():
    user_name = input("Enter User Name: ").strip()
    user = session.query(User).filter_by(name=user_name).first()
    if not user:
        print("User not found.")
        return

    date_input = input("Enter Date for the Meal Plan (YYYY-MM-DD): ").strip()
    try:
        plan_date = datetime.strptime(date_input, "%Y-%m-%d").date()
    except ValueError:
        print("Invalid date format. Please use YYYY-MM-DD.")
        return

    # Remove existing plan for that date
    session.query(MealPlan).filter_by(user_id=user.id, day=plan_date).delete()

    meal = input(f"Enter meal for {plan_date.strftime('%A')} ({plan_date}): ")
    plan = MealPlan(user=user, day=plan_date, meal=meal)
    session.add(plan)
    session.commit()

    print("\n✅ Daily Meal Plan saved successfully!")

def view_daily_meal_plan():
    user_name = input("Enter User Name: ").strip()
    user = session.query(User).filter_by(name=user_name).first()
    if not user:
        print("User not found.")
        return

    date_input = input("Enter Date to View (YYYY-MM-DD): ").strip()
    try:
        view_date = datetime.strptime(date_input, "%Y-%m-%d").date()
    except ValueError:
        print("Invalid date format. Please use YYYY-MM-DD.")
        return

    plan = session.query(MealPlan).filter_by(user_id=user.id, day=view_date).first()
    if not plan:
        print("No meal plan found for this date.")
        return

    print(f"\n🍽️ {user.name}'s Meal Plan for {view_date.strftime('%A')} ({view_date}): {plan.meal}")

# =============== MAIN MENU =====================
def main():
    while True:
        os.system("cls" if os.name == "nt" else "clear")
        print("=== Health Simplified CLI ===")
        print("1. Manage Users")
        print("2. Log/View Food Entries")
        print("3. Set/View Nutrition Goals")
        print("4. Manage Meal Plans")
        print("5. Exit")
        choice = input("Select an option: ")

        if choice == '1':
            while True:
                os.system("cls" if os.name == "nt" else "clear")
                print("1. Create User")
                print("2. List Users")
                print("3. Go Back to Main Menu")
                user_choice = input("Choice: ")
                if user_choice == '1':
                    create_user()
                elif user_choice == '2':
                    list_users()
                elif user_choice == '3':
                    break
                input("Press Enter to continue...")

        elif choice == '2':
            while True:
                os.system("cls" if os.name == "nt" else "clear")
                print("1. Add Food Entry")
                print("2. List Food Entries")
                print("3. Daily Summary Report")
                print("5. Go Back to Main Menu")
                entry_choice = input("Choice: ")
                if entry_choice == '1':
                    add_food_entry()
                elif entry_choice == '2':
                    list_food_entries()
                elif entry_choice == '3':
                    daily_summary_report()
                elif entry_choice == '5':
                    break
                input("Press Enter to continue...")

        elif choice == '3':
            while True:
                os.system("cls" if os.name == "nt" else "clear")
                print("1. Set Goals")
                print("2. List Goals")
                print("3. Go Back to Main Menu")
                goal_choice = input("Choice: ")
                if goal_choice == '1':
                    set_goals()
                elif goal_choice == '2':
                    list_goals()
                elif goal_choice == '3':
                    break
                input("Press Enter to continue...")

        elif choice == '4':
            while True:
                os.system("cls" if os.name == "nt" else "clear")
                print("1. Generate Daily Meal Plan")
                print("2. View Daily Meal Plan")
                print("3. Go Back to Main Menu")
                meal_choice = input("Choice: ")
                if meal_choice == '1':
                    generate_daily_meal_plan()
                elif meal_choice == '2':
                    view_daily_meal_plan()
                elif meal_choice == '3':
                    break
                input("Press Enter to continue...")

        elif choice == '5':
            print("Exiting. Goodbye!")
            session.close()
            break

        else:
            print("Invalid option.")
            input("Press Enter to try again...")

# =============== ENTRY POINT =====================
if __name__ == "__main__":
    main()
