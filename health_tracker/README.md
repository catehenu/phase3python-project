#  Health Simplified CLI Application

A command-line application to help users track food intake, set nutrition goals, and plan weekly meals. Built using Python, SQLAlchemy, and Typer, this project reinforces object-oriented programming, database integration, and test-driven development.

---

##  Project Purpose

This application was built as part of a hands-on software development module to practice:
Object-Oriented Programming (OOP)
SQLAlchemy ORM with SQLite or PostgreSQL
Command-line interface (CLI) development using Typer
Unit testing with pytest

---

##  Features

###  User Management
myapp user create --name <name> – Create a new user
myapp user list – List all users

###  Food Entries
myapp entry add --user <name> --food <food> --calories <int> --date <YYYY-MM-DD>
myapp entry list [--user <name>] [--date <date>]
myapp entry update --id <int> [fields...]
myapp entry delete --id <int>

###  Goals
myapp goal set --user <name> --daily <int> --weekly <int>
myapp goal list --user <name>

###  Reports
myapp report --user <name> --date <YYYY-MM-DD> – View daily nutrition summary

###  Meal Planning
myapp plan-meal --user <name> --week <int>
myapp plan-meal update --id <int> [fields...]

---

##  Installation

*Clone the repository*
```bash
git clone https://github.com/your-username/health-tracker.git
cd health-tracker