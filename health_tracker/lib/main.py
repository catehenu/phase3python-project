import os
from datetime import datetime
from config import Session
from models import User, FoodEntry, Goal, MealPlan  # Assuming you have MealPlan model defined

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
    # Check if goal already exists, update if so
    existing_goal = session.query(Goal).filter_by(user_id=user.id).first()
    if existing_goal:
        existing_goal.daily_calories = daily
        existing_goal.weekly_calories = weekly
        existing_goal.set_date = datetime.now()
        print("Goal updated successfully.")
    else:
        goal = Goal(user=user, daily_calories=daily, weekly_calories=weekly)
        session.add(goal)
        print("Goal set successfully.")
    session.commit()
    session.close()

def list_goals():
    session = Session()
    user_name = input("Enter User Name: ")
    user = session.query(User).filter_by(name=user_name).first()
    if not user:
        print("User not found.")
        session.close()
        return

    goals = session.query(Goal).filter_by(user_id=user.id).all()
    if not goals:
        print("No goals set for this user.")
    for goal in goals:
        print(f"Daily: {goal.daily_calories} | Weekly: {goal.weekly_calories} | Set On: {goal.set_date}")
    session.close()

# ========== MEAL PLAN OPERATIONS ==========
def add_meal_plan():
    session = Session()
    user_name = input("Enter User Name: ")
    user = session.query(User).filter_by(name=user_name).first()
    if not user:
        print("User not found.")
        session.close()
        return

    week_num = int(input("Enter Week Number (ISO week): "))
    meals = input("Enter Meals for the week (comma-separated): ")  # Example: "Chicken salad, Oatmeal, Pasta"
    meal_plan = MealPlan(user=user, week=week_num, meals=meals)
    session.add(meal_plan)
    session.commit()
    session.close()
    print("Meal plan added successfully.")

def list_meal_plans():
    session = Session()
    user_name = input("Enter User Name: ")
    user = session.query(User).filter_by(name=user_name).first()
    if not user:
        print("User not found.")
        session.close()
        return

    meal_plans = session.query(MealPlan).filter_by(user_id=user.id).all()
    if not meal_plans:
        print("No meal plans found for this user.")
    for plan in meal_plans:
        print(f"ID: {plan.id} | Week: {plan.week} | Meals: {plan.meals} | Created At: {plan.created_at}")
    session.close()

def update_meal_plan():
    session = Session()
    plan_id = int(input("Enter Meal Plan ID to update: "))
    meal_plan = session.query(MealPlan).filter_by(id=plan_id).first()
    if not meal_plan:
        print("Meal plan not found.")
        session.close()
        return

    new_meals = input(f"Enter new meals (currently: {meal_plan.meals}): ")
    if new_meals.strip():
        meal_plan.meals = new_meals
    session.commit()
    session.close()
    print("Meal plan updated successfully.")

# ========== MAIN MENU LOOP ==========
def main():
    while True:
        os.system("cls" if os.name == "nt" else "clear")
        print("=== Health Simplified CLI ===")
        print("1. Manage Users")
        print("2. Manage Food Entries")
        print("3. Manage Goals")
        print("4. Manage Meal Plans")
        print("5. Exit")

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
                else:
                    print("Invalid option.")
                input("Press Enter to continue...")

        elif main_choice == '2':
            while True:
                os.system("cls" if os.name == "nt" else "clear")
                print("1. Add Food Entry")
                print("2. List Food Entries")
                print("3. Back to Main Menu")
                food_choice = input("Select: ")
                if food_choice == '1':
                    add_food_entry()
                elif food_choice == '2':
                    list_food_entries()
                elif food_choice == '3':
                    break
                else:
                    print("Invalid option.")
                input("Press Enter to continue...")

        elif main_choice == '3':
            while True:
                os.system("cls" if os.name == "nt" else "clear")
                print("1. Set Goal")
                print("2. List Goals")
                print("3. Back to Main Menu")
                goal_choice = input("Select: ")
                if goal_choice == '1':
                    set_goal()
                elif goal_choice == '2':
                    list_goals()
                elif goal_choice == '3':
                    break
                else:
                    print("Invalid option.")
                input("Press Enter to continue...")

        elif main_choice == '4':
            while True:
                os.system("cls" if os.name == "nt" else "clear")
                print("1. Add Meal Plan")
                print("2. List Meal Plans")
                print("3. Update Meal Plan")
                print("4. Back to Main Menu")
                meal_choice = input("Select: ")
                if meal_choice == '1':
                    add_meal_plan()
                elif meal_choice == '2':
                    list_meal_plans()
                elif meal_choice == '3':
                    update_meal_plan()
                elif meal_choice == '4':
                    break
                else:
                    print("Invalid option.")
                input("Press Enter to continue...")

        elif main_choice == '5':
            print("Goodbye!")
            break
        else:
            print("Invalid option.")
            input("Press Enter to continue...")

if __name__ == "__main__":
    main()
