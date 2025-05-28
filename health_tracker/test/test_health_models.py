import pytest
from datetime import datetime, date
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# ✅ Adjusted import assuming models.py is in health_tracker/
from lib.models import User, FoodEntry, Goal, MealPlan

# ========== Setup Test Database ==========
@pytest.fixture(scope="module")
def test_engine():
    engine = create_engine("sqlite:///:memory:")
    User.metadata.create_all(engine)
    FoodEntry.metadata.create_all(engine)
    Goal.metadata.create_all(engine)
    MealPlan.metadata.create_all(engine)
    yield engine
    User.metadata.drop_all(engine)
    FoodEntry.metadata.drop_all(engine)
    Goal.metadata.drop_all(engine)
    MealPlan.metadata.drop_all(engine)

@pytest.fixture(scope="module")
def Session(test_engine):
    return sessionmaker(bind=test_engine)

# ========== TEST USER CRUD ==========
def test_create_user(Session):
    session = Session()
    user = User(name="Alice")
    session.add(user)
    session.commit()

    result = session.query(User).filter_by(name="Alice").first()
    assert result is not None
    assert result.name == "Alice"
    session.close()

def test_read_users(Session):
    session = Session()
    users = session.query(User).all()
    assert len(users) > 0
    session.close()

def test_update_user(Session):
    session = Session()
    user = session.query(User).filter_by(name="Alice").first()
    user.name = "Alice Smith"
    session.commit()

    updated_user = session.query(User).filter_by(name="Alice Smith").first()
    assert updated_user is not None
    session.close()

def test_delete_user(Session):
    session = Session()
    user = session.query(User).filter_by(name="Alice Smith").first()
    session.delete(user)
    session.commit()

    deleted = session.query(User).filter_by(name="Alice Smith").first()
    assert deleted is None
    session.close()

# ========== TEST FOOD ENTRY CRUD ==========
def test_add_food_entry(Session):
    session = Session()
    user = User(name="Bob")
    session.add(user)
    session.commit()

    entry = FoodEntry(
        food="Banana",
        calories=105,
        date=date.today(),
        created_at=datetime.utcnow(),
        user_id=user.id
    )
    session.add(entry)
    session.commit()

    result = session.query(FoodEntry).filter_by(food="Banana").first()
    assert result is not None
    assert result.calories == 105
    session.close()

def test_update_food_entry(Session):
    session = Session()
    entry = session.query(FoodEntry).filter_by(food="Banana").first()
    entry.calories = 110
    session.commit()

    updated = session.query(FoodEntry).filter_by(food="Banana").first()
    assert updated.calories == 110
    session.close()

def test_delete_food_entry(Session):
    session = Session()
    entry = session.query(FoodEntry).filter_by(food="Banana").first()
    session.delete(entry)
    session.commit()

    deleted = session.query(FoodEntry).filter_by(food="Banana").first()
    assert deleted is None
    session.close()

# ========== TEST GOAL CRUD ==========
def test_add_goal(Session):
    session = Session()
    user = User(name="Charlie")
    session.add(user)
    session.commit()

    goal = Goal(
        user_id=user.id,
        daily_calories=2200,
        weekly_calories=15400,
        set_date=date.today()
    )
    session.add(goal)
    session.commit()

    result = session.query(Goal).filter_by(user_id=user.id).first()
    assert result is not None
    assert result.daily_calories == 2200
    session.close()

def test_update_goal(Session):
    session = Session()
    goal = session.query(Goal).first()
    goal.daily_calories = 2000
    session.commit()

    updated = session.query(Goal).filter_by(id=goal.id).first()
    assert updated.daily_calories == 2000
    session.close()

def test_delete_goal(Session):
    session = Session()
    goal = session.query(Goal).first()
    session.delete(goal)
    session.commit()

    deleted = session.query(Goal).filter_by(id=goal.id).first()
    assert deleted is None
    session.close()

# ========== TEST MEAL PLAN CRUD ==========
def test_add_meal_plan(Session):
    session = Session()
    user = User(name="Daisy")
    session.add(user)
    session.commit()

    meal_plan = MealPlan(
        week_number=25,
        description="Salads and smoothies",
        user_id=user.id,
        created_at=datetime.utcnow()
    )
    session.add(meal_plan)
    session.commit()

    result = session.query(MealPlan).filter_by(week_number=25).first()
    assert result is not None
    assert "salads" in result.description.lower()
    session.close()

def test_update_meal_plan(Session):
    session = Session()
    plan = session.query(MealPlan).filter_by(week_number=25).first()
    plan.description = "Keto meal plan"
    session.commit()

    updated = session.query(MealPlan).filter_by(id=plan.id).first()
    assert "keto" in updated.description.lower()
    session.close()

def test_delete_meal_plan(Session):
    session = Session()
    plan = session.query(MealPlan).filter_by(week_number=25).first()
    session.delete(plan)
    session.commit()

    deleted = session.query(MealPlan).filter_by(id=plan.id).first()
    assert deleted is None
    session.close()
