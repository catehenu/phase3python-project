from faker import Faker
from datetime import datetime, date, timedelta
from sqlalchemy.sql import func
from config import session, engine  # Ensure Session and engine are defined in config.py
from models import User, FoodEntry, Goal, MealPlan

# Initialize Faker
fake = Faker()

# Create tables
User.metadata.create_all(engine)
FoodEntry.metadata.create_all(engine)
Goal.metadata.create_all(engine)
MealPlan.metadata.create_all(engine)

# Seed Users
for _ in range(5):  # Create 5 sample users
    user = User(
        name=fake.name(),
        created_at=datetime.utcnow()
    )
    session.add(user)
session.commit()

# Get all users
users = session.query(User).all()

# Seed FoodEntries, Goals, and MealPlans
for user in users:
    # Add 10 food entries
    for _ in range(10):
        food_entry = FoodEntry(
            food=fake.word(),
            calories=fake.random_int(min=100, max=800),
            date=fake.date_between(start_date='-30d', end_date='today'),
            created_at=datetime.utcnow(),
            user_id=user.id
        )
        session.add(food_entry)

    # Add 1 goal
    goal = Goal(
        daily_calories=fake.random_int(min=1800, max=2500),
        weekly_calories=fake.random_int(min=12000, max=17500),
        set_date=date.today(),
        user_id=user.id
    )
    session.add(goal)

    # Add 2 meal plans
    for i in range(2):
        meal_plan = MealPlan(
            week_number=fake.random_int(min=1, max=52),
            description=fake.sentence(nb_words=8),
            created_at=datetime.utcnow(),
            user_id=user.id
        )
        session.add(meal_plan)

# Commit all changes
session.commit()

print("Sample users, food entries, goals, and meal plans have been added successfully!")
