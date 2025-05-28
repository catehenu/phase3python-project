from sqlalchemy import Column, Integer, String, ForeignKey, Date, DateTime
from sqlalchemy.orm import declarative_base, relationship
from datetime import datetime, date

Base = declarative_base()

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    food_entries = relationship("FoodEntry", back_populates="user", cascade="all, delete-orphan")
    goals = relationship("Goal", back_populates="user", cascade="all, delete-orphan")
    meal_plans = relationship("MealPlan", back_populates="user", cascade="all, delete-orphan")

class FoodEntry(Base):
    __tablename__ = "food_entries"

    id = Column(Integer, primary_key=True)
    food = Column(String(100), nullable=False)
    calories = Column(Integer, nullable=False)
    date = Column(Date, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    user = relationship("User", back_populates="food_entries")

class Goal(Base):
    __tablename__ = "goals"

    id = Column(Integer, primary_key=True)
    daily_calories = Column(Integer, nullable=False)
    weekly_calories = Column(Integer, nullable=False)
    # Use date.today for default date (not datetime.utcnow) for date fields
    set_date = Column(Date, default=date.today, nullable=False)

    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    user = relationship("User", back_populates="goals")

class MealPlan(Base):
    __tablename__ = "meal_plans"

    id = Column(Integer, primary_key=True)
    week_number = Column(Integer, nullable=False)
    description = Column(String(255), nullable=True)  # Changed from 'meals' to 'description' for clarity
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    user = relationship("User", back_populates="meal_plans")
