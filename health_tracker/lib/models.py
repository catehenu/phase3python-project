from sqlalchemy import Column, Integer, String, Date, DateTime, ForeignKey, Text
from sqlalchemy.orm import relationship, declarative_base
from datetime import datetime

Base = declarative_base()

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    name = Column(String(50), unique=True, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    food_entries = relationship("FoodEntry", back_populates="user", cascade="all, delete-orphan")
    goals = relationship("Goal", back_populates="user", cascade="all, delete-orphan")
    meal_plans = relationship("MealPlan", back_populates="user", cascade="all, delete-orphan")

class FoodEntry(Base):
    __tablename__ = "food_entries"
    id = Column(Integer, primary_key=True)
    food = Column(String(100), nullable=False)
    calories = Column(Integer, nullable=False)
    date = Column(Date, nullable=False)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)  # ✅ Add this line
    user_id = Column(Integer, ForeignKey("users.id"))
    user = relationship("User", back_populates="food_entries")

class Goal(Base):
    __tablename__ = "goals"
    id = Column(Integer, primary_key=True)
    daily_calories = Column(Integer, nullable=False)
    weekly_calories = Column(Integer, nullable=False)
    set_date = Column(DateTime, default=datetime.utcnow)
    user_id = Column(Integer, ForeignKey("users.id"))
    user = relationship("User", back_populates="goals")

class MealPlan(Base):
    __tablename__ = "meal_plans"
    id = Column(Integer, primary_key=True)
    day = Column(Date, nullable=False)
    meal = Column(Text, nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"))
    user = relationship("User", back_populates="meal_plans")
